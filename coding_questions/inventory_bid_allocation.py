"""Priority Inventory Allocation with Round-Robin Tie Handling

A limited inventory must be allocated across customer requests. Each request contains:

    [customer_id, quantity, bid_amount, timestamp]

Allocation rules:
1. Higher bid amounts are processed before lower bid amounts.
2. Customers with the same bid are ordered by timestamp and share inventory in round-robin cycles.
3. During each cycle, an active customer receives at most one item.
4. A customer leaves the rotation once the requested quantity is fulfilled.
5. Allocation stops when inventory reaches zero.
6. Return the customer IDs that received no items, sorted in ascending order.

The important optimization is that the output asks only who received zero items. We do not need to simulate every allocated item.
Within one equal-bid group:
- If remaining inventory covers the group's total requested quantity, the whole group is fulfilled.
- If inventory is smaller than the number of customers in the group, only the earliest customers reached in the first cycle
  receive anything; the rest of that group receive zero.
- If inventory is at least the group size but smaller than the group's total requested quantity, every customer in that group
  receives at least one item before inventory is exhausted, so only lower-priority groups can still be zero-allocation customers.

Assumptions:
- Each customer appears in at most one request.
- quantity is positive.
- timestamp ordering is sufficient to break ties inside an equal-bid group. Python's stable sort preserves input order if two
  timestamps are also equal.
- total_inventory may be zero.

Algorithm:
1. Sort requests by bid descending and timestamp ascending.
2. Scan one bid group at a time.
3. Compare remaining inventory with the group's total requested quantity and group size.
4. Once inventory is guaranteed to be exhausted, append only the customers that could not have received an item, plus every
   lower-bid customer, and stop.

Complexity:
- Sorting: O(n log n).
- Group scan: O(n).
- Total: O(n log n) time and O(n) extra space for the sorted copy/result.
- This avoids O(total_inventory) round-by-round simulation, which can time out when quantities or inventory are very large.

Important edge cases:
- No inventory at all.
- Inventory is enough for every request.
- Inventory stops exactly between bid groups.
- Inventory is smaller than the number of customers tied at the current bid.
- Inventory allows at least one item per tied customer but not full fulfillment.
- Multiple equal bids with different timestamps.
- One very large quantity should not force per-item looping.

Common debugging failure modes:
- A grouped while-loop whose boundary variable never advances can create an infinite loop and timeout.
- Incrementing the outer index while trying to find the end of a group can corrupt the scan state.
- Simulating one item at a time is correct conceptually but unnecessary for this output and can be far too slow.
"""

from __future__ import annotations

from typing import Iterable, Sequence

Request = tuple[int, int, int, int]


def _normalize_requests(requests: Iterable[Sequence[int]]) -> list[Request]:
    normalized: list[Request] = []

    for request in requests:
        if len(request) != 4:
            raise ValueError(
                "Each request must contain customer_id, quantity, bid_amount, and timestamp"
            )

        customer_id, quantity, bid_amount, timestamp = map(int, request)
        if quantity <= 0:
            raise ValueError("Requested quantity must be positive")

        normalized.append((customer_id, quantity, bid_amount, timestamp))

    return normalized


def get_unfulfilled_customers(
    requests: Iterable[Sequence[int]],
    total_inventory: int,
) -> list[int]:
    """Return customer IDs that receive zero items."""
    ordered = sorted(
        _normalize_requests(requests),
        key=lambda request: (-request[2], request[3]),
    )

    if total_inventory <= 0:
        return sorted(customer_id for customer_id, _, _, _ in ordered)

    remaining = total_inventory
    request_count = len(ordered)
    group_start = 0

    while group_start < request_count:
        if remaining <= 0:
            return sorted(customer_id for customer_id, _, _, _ in ordered[group_start:])

        bid_amount = ordered[group_start][2]
        group_end = group_start
        group_total = 0

        while group_end < request_count and ordered[group_end][2] == bid_amount:
            group_total += ordered[group_end][1]
            group_end += 1

        if remaining >= group_total:
            remaining -= group_total
            group_start = group_end
            continue

        group_size = group_end - group_start

        if remaining < group_size:
            unfulfilled = [
                customer_id for customer_id, _, _, _ in ordered[group_start + remaining : group_end]
            ]
            unfulfilled.extend(customer_id for customer_id, _, _, _ in ordered[group_end:])
            return sorted(unfulfilled)

        return sorted(customer_id for customer_id, _, _, _ in ordered[group_end:])

    return []


def getUnfulfilledCustomers(requests, totalInventory):
    """Compatibility wrapper matching a common coding-platform signature."""
    return get_unfulfilled_customers(requests, totalInventory)


def run_sample_tests() -> None:
    requests = [
        [1, 5, 5, 0],
        [2, 7, 8, 1],
        [3, 7, 5, 1],
        [4, 10, 3, 3],
    ]
    assert get_unfulfilled_customers(requests, 18) == [4]

    sample = [
        [1, 2, 5, 0],
        [2, 1, 4, 2],
        [3, 5, 4, 6],
    ]
    assert get_unfulfilled_customers(sample, 3) == [3]

    tied = [
        [10, 5, 9, 30],
        [11, 5, 9, 10],
        [12, 5, 9, 20],
        [13, 1, 8, 1],
    ]
    assert get_unfulfilled_customers(tied, 2) == [10, 13]
    assert get_unfulfilled_customers(tied, 3) == [13]
    assert get_unfulfilled_customers(tied, 8) == [13]
    assert get_unfulfilled_customers(tied, 16) == []
    assert get_unfulfilled_customers(tied, 0) == [10, 11, 12, 13]

    print("All priority inventory allocation sample tests passed.")


if __name__ == "__main__":
    run_sample_tests()


"""
Alternative approach:
A literal round-robin simulator can keep each equal-bid group in timestamp order and repeatedly give one item to each active request.
That is easy to explain, but its runtime depends on the number of items allocated and can approach O(total_inventory), which is unsafe
when quantities are large. The optimized solution reasons about the first cycle and group totals because the required output is only the
set of customers who received nothing.

Explanation:
1. Sorting establishes the global priority order: higher bid first, then earlier timestamp inside a tie.
2. A fully coverable bid group can be skipped with one subtraction rather than simulating every item.
3. If remaining inventory is less than the group size, the first round determines exactly which tied customers receive zero items.
4. If remaining inventory reaches every customer in the current group at least once, nobody in that group belongs in the output even
   though some requested quantities may remain unfilled.
5. Once inventory is exhausted inside a group, every lower-bid customer receives zero and the algorithm can terminate immediately.

Summary:
- Optimize for the output actually requested rather than simulating unnecessary state.
- Group equal-priority records after sorting.
- Maintain clear pointer-progress invariants in nested scans.
- Separate "request not fully satisfied" from "received no items"; they are different conditions.
"""
