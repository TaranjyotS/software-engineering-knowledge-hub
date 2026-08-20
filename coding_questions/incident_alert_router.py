"""Incident Alert Router and Retry Backoff

We are building the backend for an incident-alerting service. Each Alert represents a reported problem for a service and has
an alert ID, service, severity, created time, optional resolved time, and zero or more delivery attempts made to on-call
responders. The AlertRouter manages all alerts for the current on-call window.

The exercise has three parts:

1. Fix has_open_alert(service). It should return True when the service has at least one unresolved alert. A resolved alert for
   the same service must not cause an early False if another alert for that service is still open.
2. Add delivery-attempt tracking. record_attempt(alert_id, attempt) stores the attempt only if the alert exists and returns a
   boolean indicating whether it was recorded. get_attempt_counts() returns {alert_id: count} only for alerts that have at
   least one attempt.
3. Implement get_backoff_violations(cooldown). Retry policy requires consecutive attempts for the same alert to be at least
   cooldown minutes apart. Attempts exactly cooldown minutes apart are allowed. Return the sorted IDs of alerts that contain
   at least one pair of consecutive attempts whose time gap is strictly less than cooldown.

Input / domain objects:
- Alert(alert_id, service, severity, created_at, resolved_at=None)
- DeliveryAttempt(responder, attempted_at)

Expected behavior:
- has_open_alert(service) -> bool
- record_attempt(alert_id, attempt) -> bool
- get_attempt_counts() -> dict[int, int]
- get_backoff_violations(cooldown) -> sorted list[int]

Key observations:
- Return False from has_open_alert only after scanning all relevant alerts.
- Each Alert must own a separate delivery_attempts list; field(default_factory=list) avoids shared mutable state.
- Once attempts are sorted chronologically, comparing adjacent pairs is sufficient to detect any retry-policy violation.
- Use gap < cooldown rather than gap <= cooldown, and add each violating alert ID only once.

Complexity:
- has_open_alert and record_attempt are O(a), where a is the number of alerts.
- get_attempt_counts is O(a).
- get_backoff_violations is O(sum(m_i log m_i)) because each alert's attempts are sorted before adjacent comparisons.

Important edge cases include no alerts for a service, a resolved alert before a later open alert, unknown alert IDs, zero or one
delivery attempt, attempts arriving out of order, a gap exactly equal to cooldown, and multiple violations for one alert.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Severity(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass(frozen=True)
class DeliveryAttempt:
    responder: str
    attempted_at: int


@dataclass
class Alert:
    alert_id: int
    service: str
    severity: Severity
    created_at: int
    resolved_at: int | None = None
    delivery_attempts: list[DeliveryAttempt] = field(default_factory=list)


class AlertRouter:
    def __init__(self) -> None:
        self.alerts: list[Alert] = []

    def add_alert(self, alert: Alert) -> None:
        self.alerts.append(alert)

    def get_alert(self, alert_id: int) -> Alert | None:
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                return alert
        return None

    def has_open_alert(self, service: str) -> bool:
        """Return whether any alert for the service is currently open."""
        for alert in self.alerts:
            if alert.service == service and alert.resolved_at is None:
                return True
        return False

    def record_attempt(self, alert_id: int, attempt: DeliveryAttempt) -> bool:
        """Associate an attempt with an existing alert."""
        alert = self.get_alert(alert_id)
        if alert is None:
            return False

        alert.delivery_attempts.append(attempt)
        return True

    def get_attempt_counts(self) -> dict[int, int]:
        """Return counts only for alerts that have at least one attempt."""
        return {
            alert.alert_id: len(alert.delivery_attempts)
            for alert in self.alerts
            if alert.delivery_attempts
        }

    def get_backoff_violations(self, cooldown: int) -> list[int]:
        """Return sorted IDs with adjacent attempts closer than cooldown."""
        violations: list[int] = []

        for alert in self.alerts:
            attempts = sorted(
                alert.delivery_attempts,
                key=lambda attempt: attempt.attempted_at,
            )

            for previous, current in zip(attempts, attempts[1:]):
                if current.attempted_at - previous.attempted_at < cooldown:
                    violations.append(alert.alert_id)
                    break

        return sorted(violations)


def run_sample_tests() -> None:
    router = AlertRouter()
    router.add_alert(
        Alert(
            alert_id=1,
            service="payments",
            severity=Severity.HIGH,
            created_at=0,
            resolved_at=5,
        )
    )
    router.add_alert(
        Alert(
            alert_id=2,
            service="payments",
            severity=Severity.CRITICAL,
            created_at=10,
        )
    )
    router.add_alert(
        Alert(
            alert_id=3,
            service="search",
            severity=Severity.MEDIUM,
            created_at=15,
        )
    )

    # A resolved alert appearing first must not hide a later open alert.
    assert router.has_open_alert("payments")
    assert not router.has_open_alert("unknown")

    for minute in (0, 10, 20):
        assert router.record_attempt(1, DeliveryAttempt("alice", minute))
    for minute in (0, 3):
        assert router.record_attempt(2, DeliveryAttempt("bob", minute))

    assert not router.record_attempt(500, DeliveryAttempt("carol", 7))
    assert router.get_attempt_counts() == {1: 3, 2: 2}
    assert router.get_backoff_violations(5) == [2]

    # A gap exactly equal to cooldown is allowed.
    router.record_attempt(3, DeliveryAttempt("dana", 0))
    router.record_attempt(3, DeliveryAttempt("dana", 5))
    assert router.get_backoff_violations(5) == [2]

    print("All incident alert router sample tests passed.")


if __name__ == "__main__":
    run_sample_tests()

"""
Explanation:
1. has_open_alert scans until it finds an alert whose service matches and whose resolved_at value is None. The False return is
   outside the loop, which fixes the early-return bug where a resolved alert could hide a later open alert for the same service.
2. record_attempt reuses get_alert so an attempt is appended only to a valid alert. Because delivery_attempts is created with
   field(default_factory=list), every Alert instance owns its own independent list.
3. get_attempt_counts includes only alerts whose attempt list is non-empty.
4. get_backoff_violations sorts each alert's attempts by attempted_at and compares adjacent attempts. If an adjacent gap is
   smaller than cooldown, the alert ID is added once and processing for that alert stops.

Summary:
- Scan fully before returning a negative result when later records may satisfy the condition.
- Keep mutable state per entity rather than sharing one list across instances.
- Sorting plus adjacent-pair comparison is a simple and reliable way to validate retry spacing.
- A gap equal to cooldown is valid; only a strictly smaller gap violates the policy.
"""
