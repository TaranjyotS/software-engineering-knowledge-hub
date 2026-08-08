'''Issue Creation Workflow: Persistence, Nested Issues, Authentication, and Sequential Identifiers

A backend repository contains a broken POST endpoint for creating issues and sub-issues. The handler parses the request body, computes an
identifier, and returns HTTP 201, but it never persists a record. The authentication wrapper also has a special-case branch for issue
routes that returns an empty 401 response, while the API contract requires a normal error message.

Generalized requirements:
1. Authentication is required. Missing authentication returns 401 with a message.
2. title is required and must contain non-whitespace text. Missing title returns 400 with a message containing "required".
3. teamId must refer to an existing team. An unknown team returns 404 with "Team not found".
4. The creator comes from the authenticated user, not a caller-controlled creator field.
5. Each issue receives a team-local identifier in the form TEAM_KEY-N, where N increases independently for each team.
6. description, status, priority, assignee, labels, and parentIssue are optional.
7. A sub-issue uses the same create endpoint but includes parentIssue. The parent must exist and belong to the same team.
8. A created issue is persisted before returning 201.
9. Creation records an activity entry with action "created".
10. The success response contains an issue object, including its team and parentIssue relationship where applicable.

This standalone exercise uses in-memory repositories so it can run without a web framework. In a Django implementation, the same logic
maps to request.user, model lookups, transaction.atomic(), Issue.objects.create(...), Activity.objects.create(...), and issue.to_dict().

Debugging approach:
- Read failing tests first to extract the exact API contract.
- Trace route -> authentication/middleware -> handler -> model fields -> serializer/response.
- Compare the create path with a working update/read path for established lookup and serialization patterns.
- Search for early returns before persistence and for input fields that are parsed but never used.
- Check error response shape as well as status code; `{}` with 401 is not equivalent to `{ "message": ... }` with 401.

Key observations:
- Returning the correct status code before saving is still a functional failure.
- Global count()+1 is not a correct source for a team-local identifier.
- count()+1 or max()+1 is also vulnerable to concurrent duplicate allocation unless identifier generation is serialized or protected by a
  database uniqueness constraint plus retry.
- Authentication identity should be authoritative for creator/audit fields.
- Parent-child integrity belongs in the trusted application/data layer, not only in the UI.

Complexity for this in-memory implementation:
- Team/user/issue lookup is O(1) average via dictionaries.
- Identifier allocation is O(1) using a per-team next-number map.
- Creation is O(1) average plus O(len(labels)) to copy labels.
- Stored state is O(t + u + i + a) for teams, users, issues, and activities.

Important edge cases:
- Missing/blank title.
- Unknown team.
- Missing auth.
- Unknown assignee.
- Unknown parent issue.
- Parent issue from another team.
- Independent numbering for multiple teams.
- Sub-issue identifier sharing the same team sequence as top-level issues.
- Caller attempts to spoof creator.
- Successful response is returned only after persistence and activity creation.
'''

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class User:
    user_id: str
    name: str


@dataclass(frozen=True)
class Team:
    team_id: str
    name: str
    key: str


@dataclass
class Issue:
    issue_id: str
    identifier: str
    title: str
    team: Team
    creator: User
    description: str = ""
    status: str = "todo"
    priority: str = "no_priority"
    assignee: User | None = None
    parent_issue_id: str | None = None
    labels: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "_id": self.issue_id,
            "identifier": self.identifier,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "team": {
                "_id": self.team.team_id,
                "name": self.team.name,
                "key": self.team.key,
            },
            "assignee": self.assignee.user_id if self.assignee else None,
            "creator": self.creator.user_id,
            "parentIssue": self.parent_issue_id,
            "labels": list(self.labels),
        }


@dataclass(frozen=True)
class Activity:
    issue_id: str
    user_id: str
    action: str


@dataclass(frozen=True)
class Response:
    status: int
    body: dict[str, Any]


class IssueService:
    def __init__(self) -> None:
        self.users: dict[str, User] = {}
        self.teams: dict[str, Team] = {}
        self.issues: dict[str, Issue] = {}
        self.activities: list[Activity] = []
        self._next_issue_id = 1
        self._next_number_by_team: dict[str, int] = {}

    def add_user(self, user: User) -> None:
        self.users[user.user_id] = user

    def add_team(self, team: Team) -> None:
        self.teams[team.team_id] = team

    def _next_identifier(self, team: Team) -> str:
        number = self._next_number_by_team.get(team.team_id, 1)
        self._next_number_by_team[team.team_id] = number + 1
        return f"{team.key}-{number}"

    def create_issue(self, payload: dict[str, Any], actor: User) -> Response:
        title = str(payload.get("title", "")).strip()
        if not title:
            return Response(400, {"message": "Title is required"})

        team_id = payload.get("teamId")
        team = self.teams.get(str(team_id)) if team_id is not None else None
        if team is None:
            return Response(404, {"message": "Team not found"})

        assignee: User | None = None
        assignee_id = payload.get("assignee")
        if assignee_id:
            assignee = self.users.get(str(assignee_id))
            if assignee is None:
                return Response(404, {"message": "Assignee not found"})

        parent_issue_id = payload.get("parentIssue")
        if parent_issue_id:
            parent = self.issues.get(str(parent_issue_id))
            if parent is None:
                return Response(404, {"message": "Parent issue not found"})
            if parent.team.team_id != team.team_id:
                return Response(400, {"message": "Parent issue must belong to the same team"})
            parent_issue_id = parent.issue_id
        else:
            parent_issue_id = None

        issue_id = str(self._next_issue_id)
        self._next_issue_id += 1

        issue = Issue(
            issue_id=issue_id,
            identifier=self._next_identifier(team),
            title=title,
            description=str(payload.get("description") or ""),
            status=str(payload.get("status") or "todo"),
            priority=str(payload.get("priority") or "no_priority"),
            team=team,
            assignee=assignee,
            creator=actor,
            parent_issue_id=parent_issue_id,
            labels=list(payload.get("labels") or []),
        )

        # Persist before forming the success response.
        self.issues[issue.issue_id] = issue
        self.activities.append(
            Activity(issue_id=issue.issue_id, user_id=actor.user_id, action="created")
        )

        return Response(201, {"issue": issue.to_dict()})


def handle_create_issue(
    service: IssueService,
    payload: dict[str, Any],
    authenticated_user_id: str | None,
) -> Response:
    """Small transport-level wrapper that models authentication behavior."""
    if not authenticated_user_id:
        return Response(401, {"message": "Authentication required"})

    actor = service.users.get(authenticated_user_id)
    if actor is None:
        return Response(401, {"message": "User not found"})

    return service.create_issue(payload, actor)


def run_sample_tests() -> None:
    service = IssueService()
    alice = User("u1", "Alice")
    bob = User("u2", "Bob")
    service.add_user(alice)
    service.add_user(bob)
    service.add_team(Team("team-a", "Platform", "PLT"))
    service.add_team(Team("team-b", "Data", "DAT"))

    unauthenticated = handle_create_issue(
        service,
        {"title": "First issue", "teamId": "team-a"},
        None,
    )
    assert unauthenticated.status == 401
    assert "message" in unauthenticated.body

    missing_title = handle_create_issue(service, {"teamId": "team-a"}, "u1")
    assert missing_title.status == 400
    assert "required" in missing_title.body["message"].lower()

    missing_team = handle_create_issue(
        service,
        {"title": "First issue", "teamId": "missing"},
        "u1",
    )
    assert missing_team == Response(404, {"message": "Team not found"})

    first = handle_create_issue(
        service,
        {
            "title": "Create API contract",
            "teamId": "team-a",
            "status": "todo",
            "priority": "high",
            "assignee": "u2",
            "labels": ["backend", "api"],
            "creator": "spoofed-user",
        },
        "u1",
    )
    assert first.status == 201
    first_issue = first.body["issue"]
    assert first_issue["identifier"] == "PLT-1"
    assert first_issue["creator"] == "u1"
    assert first_issue["assignee"] == "u2"
    assert first_issue["team"]["key"] == "PLT"

    second = handle_create_issue(
        service,
        {"title": "Add validation", "teamId": "team-a"},
        "u1",
    )
    assert second.body["issue"]["identifier"] == "PLT-2"

    other_team = handle_create_issue(
        service,
        {"title": "Build pipeline", "teamId": "team-b"},
        "u1",
    )
    assert other_team.body["issue"]["identifier"] == "DAT-1"

    child = handle_create_issue(
        service,
        {
            "title": "Nested validation task",
            "teamId": "team-a",
            "parentIssue": first_issue["_id"],
        },
        "u2",
    )
    assert child.status == 201
    assert child.body["issue"]["identifier"] == "PLT-3"
    assert child.body["issue"]["parentIssue"] == first_issue["_id"]

    cross_team_child = handle_create_issue(
        service,
        {
            "title": "Invalid nested task",
            "teamId": "team-b",
            "parentIssue": first_issue["_id"],
        },
        "u2",
    )
    assert cross_team_child.status == 400

    assert len(service.issues) == 4
    assert len(service.activities) == 4
    assert all(activity.action == "created" for activity in service.activities)

    print("All issue creation workflow sample tests passed.")


if __name__ == "__main__":
    run_sample_tests()


'''
Alternative production implementation:
- In Django, put creation inside transaction.atomic().
- Use a dedicated per-team sequence row/counter and select_for_update(), a database-native sequence strategy, or another serialized
  allocator. Keep a unique constraint on identifier and retry serialization/uniqueness conflicts when appropriate.
- Do not rely on Issue.objects.count() + 1: it is global rather than team-local, can reuse numbers after deletion, and races under
  concurrent requests.
- Load team, optional assignee, and optional parent through guarded queries that map DoesNotExist to explicit API errors.
- Set creator=request.user regardless of any caller-provided creator field.
- Save the issue, create the activity record, then reload/select_related as needed before serializing the response.
- Keep middleware/decorator authentication responses consistent across routes unless the API contract explicitly documents otherwise.

Explanation:
1. The transport wrapper enforces authentication before creation and returns a consistent error body.
2. The service validates required fields and foreign-key-like references before mutating state.
3. A per-team counter produces independent PLT-1, PLT-2, DAT-1 style identifiers.
4. The authenticated actor becomes creator, preventing request-body identity spoofing.
5. parentIssue uses the same create path and is validated as a same-team relationship.
6. Persistence and activity creation happen before the success response is constructed.

Summary:
- Trace failed create requests end to end rather than patching only the visible symptom.
- Treat tests as executable API contracts for status, body shape, persistence, and relationships.
- Never return success before the durable side effect has occurred.
- Keep business identifier allocation concurrency-safe in production.
- Use authenticated identity for audit-sensitive fields.
'''
