"""Kubernetes Job Reconciliation: Compare Cluster and Database Pod State.

Question
--------
An application stores a database snapshot of the Kubernetes pods registered to
each job. A pod is uniquely identified by ``(namespace, name)``. Build a service
that receives a job ID and determines whether every pod currently returned by
Kubernetes is already present in the job's database snapshot.

The submitted live-coding version compared ``Pod`` instances by object identity,
so two separately constructed objects representing the same Kubernetes pod were
considered different. It also queried both dependencies twice when the caller
asked for the Boolean result and then requested the missing pods. This completed
version uses value objects, performs one snapshot read, and reports both missing
and stale database entries.

Requirements
------------
1. Treat namespace plus name as the stable pod identity.
2. Report pods present in Kubernetes but missing from the database.
3. Also report stale database pods that Kubernetes no longer returns.
4. Define ``is_complete`` according to the original requirement: no Kubernetes
   pod is missing. Extra stale database rows do not make it false.
5. Define ``is_exact`` for callers that require both snapshots to match.
6. Raise a controlled error when the job does not exist.
7. Read the database job and Kubernetes pod list once per reconciliation.

Complexity
----------
For ``k`` Kubernetes pods and ``d`` database pods, reconciliation is
``O(k + d)`` time and ``O(k + d)`` auxiliary space.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, Sequence


@dataclass(frozen=True, order=True, slots=True)
class Pod:
    """A Kubernetes pod value object identified by namespace and name."""

    namespace: str
    name: str

    def __post_init__(self) -> None:
        """Reject identities that Kubernetes could not use reliably."""
        if not self.namespace.strip() or not self.name.strip():
            raise ValueError("Pod namespace and name must be non-empty")


@dataclass(frozen=True, slots=True)
class Job:
    """Application job and the pods stored in its database snapshot."""

    job_id: str
    label: str
    registered_pods: tuple[Pod, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """Require the fields needed to query Kubernetes."""
        if not self.job_id.strip() or not self.label.strip():
            raise ValueError("Job ID and label must be non-empty")


class JobNotFoundError(LookupError):
    """Raised when the requested job is absent from the application database."""


class DatabaseClient(Protocol):
    """Minimum database dependency required by the reconciliation service."""

    def find_job_by_id(self, job_id: str) -> Job | None:
        """Return a job snapshot, or ``None`` when the ID does not exist."""


class KubernetesClient(Protocol):
    """Minimum Kubernetes dependency required by the reconciliation service."""

    def get_pods(self, job_id: str, label: str) -> Sequence[Pod]:
        """Return the current cluster pods associated with a job."""


@dataclass(frozen=True, slots=True)
class ReconciliationReport:
    """Differences between one Kubernetes read and one database snapshot read."""

    job_id: str
    missing_in_database: tuple[Pod, ...]
    stale_in_database: tuple[Pod, ...]

    @property
    def is_complete(self) -> bool:
        """Return whether the database contains every current Kubernetes pod."""
        return not self.missing_in_database

    @property
    def is_exact(self) -> bool:
        """Return whether neither snapshot contains an unmatched pod."""
        return self.is_complete and not self.stale_in_database


class JobReconciliationService:
    """Compare stored and live pod sets without performing synchronization writes."""

    def __init__(
        self,
        database_client: DatabaseClient,
        kubernetes_client: KubernetesClient,
    ) -> None:
        """Inject clients so the reconciliation logic remains easy to test."""
        self.database_client = database_client
        self.kubernetes_client = kubernetes_client

    def reconcile(self, job_id: str) -> ReconciliationReport:
        """Return the complete bidirectional difference for ``job_id``.

        Duplicate rows are collapsed because Kubernetes pod identity is a set
        concept here. The returned tuples are sorted to make logs and tests
        deterministic.
        """
        normalized_job_id = job_id.strip()
        if not normalized_job_id:
            raise ValueError("Job ID must be non-empty")

        job = self.database_client.find_job_by_id(normalized_job_id)
        if job is None:
            raise JobNotFoundError(f"Job not found: {normalized_job_id}")

        database_pods = set(job.registered_pods)
        kubernetes_pods = set(self.kubernetes_client.get_pods(job.job_id, job.label))

        return ReconciliationReport(
            job_id=job.job_id,
            missing_in_database=tuple(sorted(kubernetes_pods - database_pods)),
            stale_in_database=tuple(sorted(database_pods - kubernetes_pods)),
        )


class InMemoryDatabaseClient:
    """Small database fake used by the examples and tests."""

    def __init__(self, jobs: Sequence[Job]) -> None:
        """Index supplied jobs by ID."""
        self.jobs = {job.job_id: job for job in jobs}
        self.read_count = 0

    def find_job_by_id(self, job_id: str) -> Job | None:
        """Return a stored job and record the dependency call."""
        self.read_count += 1
        return self.jobs.get(job_id)


class InMemoryKubernetesClient:
    """Small Kubernetes fake keyed by job ID."""

    def __init__(self, pods_by_job: dict[str, Sequence[Pod]]) -> None:
        """Copy pod sequences so tests cannot mutate client state accidentally."""
        self.pods_by_job = {job_id: tuple(pods) for job_id, pods in pods_by_job.items()}
        self.read_count = 0

    def get_pods(self, job_id: str, label: str) -> Sequence[Pod]:
        """Return current pods; ``label`` mirrors a real selector dependency."""
        del label
        self.read_count += 1
        return self.pods_by_job.get(job_id, ())


def _run_examples() -> None:
    """Exercise equality, directionality, namespaces, and dependency call count."""
    stored_job = Job(
        job_id="job-1",
        label="training-job",
        registered_pods=(
            Pod(namespace="mlops", name="pod-1"),
            Pod(namespace="dev", name="pod-2"),
        ),
    )
    database = InMemoryDatabaseClient([stored_job])
    kubernetes = InMemoryKubernetesClient(
        {
            "job-1": (
                Pod(namespace="mlops", name="pod-1"),
                Pod(namespace="mlops", name="pod-2"),
            )
        }
    )
    service = JobReconciliationService(database, kubernetes)

    report = service.reconcile("job-1")
    assert report.missing_in_database == (Pod(namespace="mlops", name="pod-2"),)
    assert report.stale_in_database == (Pod(namespace="dev", name="pod-2"),)
    assert not report.is_complete
    assert not report.is_exact
    assert database.read_count == 1
    assert kubernetes.read_count == 1

    superset_database = InMemoryDatabaseClient([stored_job])
    one_live_pod = InMemoryKubernetesClient({"job-1": (Pod(namespace="mlops", name="pod-1"),)})
    superset_report = JobReconciliationService(
        superset_database,
        one_live_pod,
    ).reconcile("job-1")
    assert superset_report.is_complete
    assert not superset_report.is_exact

    try:
        service.reconcile("unknown-job")
    except JobNotFoundError:
        pass
    else:
        raise AssertionError("Unknown jobs must raise JobNotFoundError")


if __name__ == "__main__":
    _run_examples()
    print("Kubernetes job reconciliation examples passed.")
