"""Match Statistics and Head-to-Head History

Build a game manager that stores registered players and match results. The system should validate incoming results, calculate
per-player statistics, calculate average scores grouped by outcome, and summarize head-to-head history between two players.

A real match is represented by two MatchResult records: one from each player's perspective. For example, if Alice beats Bob,
one record says Alice had a WIN against Bob and the mirrored record says Bob had a LOSS against Alice.

Requirements:
1. Ignore or reject match results that reference a player or opponent that has not been registered.
2. get_player_statistics(player_id) returns total matches, wins, losses, draws, and win rate. Draws still count toward the total
   number of matches, so total_matches must not be calculated as only wins + losses.
3. get_average_score_by_outcome(player_id) returns the player's average score for every outcome that actually occurred.
4. summarize_head_to_head(player1_id, player2_id) returns wins for player 1, wins for player 2, draws, total matches, the
   latest result from player 1's perspective, and the latest match timestamp.

Key observations:
- A set gives O(1) average membership checks when validating player IDs.
- Totals and counts dictionaries allow average scores to be calculated in one pass.
- Mirrored result records must not be double counted. Looking only at player1 -> player2 records counts each real match once.
- The latest match should be selected by timestamp rather than assuming records arrived in chronological order.

Complexity:
- Adding a valid result is O(1).
- Player statistics, average score by outcome, and head-to-head summaries are O(n), where n is the number of stored result
  records. The implementation favors interview readability over more aggressive indexing.

Important edge cases include unknown players, players with no matches, only draws, repeated opponents, no history between the
requested pair, and records arriving out of timestamp order.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Outcome(str, Enum):
    WIN = "win"
    LOSS = "loss"
    DRAW = "draw"


@dataclass(frozen=True)
class MatchResult:
    player_id: str
    opponent_id: str
    outcome: Outcome
    score: int
    timestamp: int


@dataclass(frozen=True)
class PlayerStatistics:
    total_matches: int
    wins: int
    losses: int
    draws: int
    win_rate: float


@dataclass(frozen=True)
class HeadToHead:
    player1_id: str
    player2_id: str
    wins_player1: int = 0
    wins_player2: int = 0
    draws: int = 0
    total_matches: int = 0
    last_result: Outcome | None = None
    last_match_timestamp: int | None = None


class GameManager:
    def __init__(self) -> None:
        self.players: set[str] = set()
        self.match_results: list[MatchResult] = []

    def add_player(self, player_id: str) -> None:
        self.players.add(player_id)

    def add_match_result(self, match_result: MatchResult) -> bool:
        """Store a result only when both referenced players are registered."""
        if (
            match_result.player_id not in self.players
            or match_result.opponent_id not in self.players
        ):
            return False

        self.match_results.append(match_result)
        return True

    def record_match(
        self,
        player1_id: str,
        player2_id: str,
        player1_score: int,
        player2_score: int,
        timestamp: int,
    ) -> bool:
        """Record one real match as one result from each player's perspective."""
        if player1_id not in self.players or player2_id not in self.players:
            return False

        if player1_score > player2_score:
            player1_outcome, player2_outcome = Outcome.WIN, Outcome.LOSS
        elif player1_score < player2_score:
            player1_outcome, player2_outcome = Outcome.LOSS, Outcome.WIN
        else:
            player1_outcome = player2_outcome = Outcome.DRAW

        self.match_results.extend(
            [
                MatchResult(
                    player_id=player1_id,
                    opponent_id=player2_id,
                    outcome=player1_outcome,
                    score=player1_score,
                    timestamp=timestamp,
                ),
                MatchResult(
                    player_id=player2_id,
                    opponent_id=player1_id,
                    outcome=player2_outcome,
                    score=player2_score,
                    timestamp=timestamp,
                ),
            ]
        )
        return True

    def get_player_statistics(self, player_id: str) -> PlayerStatistics:
        player_matches = [result for result in self.match_results if result.player_id == player_id]

        wins = sum(result.outcome == Outcome.WIN for result in player_matches)
        losses = sum(result.outcome == Outcome.LOSS for result in player_matches)
        draws = sum(result.outcome == Outcome.DRAW for result in player_matches)

        # Draws still count as matches, so use all player results.
        total_matches = len(player_matches)
        win_rate = wins / total_matches if total_matches else 0.0

        return PlayerStatistics(
            total_matches=total_matches,
            wins=wins,
            losses=losses,
            draws=draws,
            win_rate=win_rate,
        )

    def get_average_score_by_outcome(self, player_id: str) -> dict[Outcome, float]:
        totals: dict[Outcome, int] = {}
        counts: dict[Outcome, int] = {}

        for result in self.match_results:
            if result.player_id != player_id:
                continue

            totals[result.outcome] = totals.get(result.outcome, 0) + result.score
            counts[result.outcome] = counts.get(result.outcome, 0) + 1

        return {outcome: totals[outcome] / counts[outcome] for outcome in totals}

    def summarize_head_to_head(
        self,
        player1_id: str,
        player2_id: str,
    ) -> HeadToHead:
        """Summarize matches once by reading only player1's perspective."""
        matches = [
            result
            for result in self.match_results
            if result.player_id == player1_id and result.opponent_id == player2_id
        ]

        if not matches:
            return HeadToHead(player1_id=player1_id, player2_id=player2_id)

        wins_player1 = sum(result.outcome == Outcome.WIN for result in matches)
        wins_player2 = sum(result.outcome == Outcome.LOSS for result in matches)
        draws = sum(result.outcome == Outcome.DRAW for result in matches)
        latest = max(matches, key=lambda result: result.timestamp)

        return HeadToHead(
            player1_id=player1_id,
            player2_id=player2_id,
            wins_player1=wins_player1,
            wins_player2=wins_player2,
            draws=draws,
            total_matches=len(matches),
            last_result=latest.outcome,
            last_match_timestamp=latest.timestamp,
        )


def run_sample_tests() -> None:
    manager = GameManager()
    for player_id in ("alice", "bob", "carol"):
        manager.add_player(player_id)

    assert manager.record_match("alice", "bob", 10, 7, 100)
    assert manager.record_match("alice", "bob", 4, 4, 200)
    assert manager.record_match("alice", "bob", 3, 8, 300)
    assert manager.record_match("alice", "carol", 6, 1, 400)
    assert not manager.record_match("alice", "unknown", 1, 0, 500)

    statistics = manager.get_player_statistics("alice")
    assert statistics == PlayerStatistics(
        total_matches=4,
        wins=2,
        losses=1,
        draws=1,
        win_rate=0.5,
    )

    averages = manager.get_average_score_by_outcome("alice")
    assert averages == {
        Outcome.WIN: 8.0,
        Outcome.DRAW: 4.0,
        Outcome.LOSS: 3.0,
    }

    head_to_head = manager.summarize_head_to_head("alice", "bob")
    assert head_to_head == HeadToHead(
        player1_id="alice",
        player2_id="bob",
        wins_player1=1,
        wins_player2=1,
        draws=1,
        total_matches=3,
        last_result=Outcome.LOSS,
        last_match_timestamp=300,
    )

    assert manager.summarize_head_to_head("bob", "carol").total_matches == 0
    print("All match statistics sample tests passed.")


if __name__ == "__main__":
    run_sample_tests()

"""
Explanation:
1. GameManager keeps registered player IDs in a set and stores MatchResult records in a list. Validation prevents results for
   unknown players from entering the system.
2. get_player_statistics filters the requested player's records, counts each outcome, and uses len(player_matches) for the
   total so draws are included. Win rate is wins / total_matches when at least one match exists.
3. get_average_score_by_outcome maintains a running total and count for each outcome and returns only outcomes the player has
   actually experienced.
4. summarize_head_to_head reads only player1's perspective of the mirrored data so each real match is counted once. A WIN is a
   player1 win, a LOSS is a player2 win, and a DRAW increments the draw count. max(..., key=timestamp) finds the latest match.

Summary:
- Validate references before storing domain records.
- Use totals plus counts for grouped averages.
- Be careful with mirrored or duplicated representations of the same real-world event.
- Prefer explicit timestamps over insertion order when determining the latest event.
"""
