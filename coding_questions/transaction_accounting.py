'''Transaction Accounting and Fee Rules

Build a transaction manager that stores deposits and withdrawals for multiple accounts and supports balance calculation,
per-account average transaction amounts, and a chronological fee policy.

Requirements:
1. get_balance(account_id) calculates the current balance for one account. Deposits increase the balance and withdrawals
   decrease it. The transaction type determines the operation rather than relying on the sign of the amount.
2. get_average_transaction_amount_by_account() returns the average absolute transaction amount for every account. Use
   abs(amount), maintain totals and counts per account, and divide after processing the transactions.
3. get_transaction_fees() applies fees independently per account in chronological order. The first three transactions for an
   account are free. Beginning with the fourth transaction, a deposit costs $1 and a withdrawal costs $2. Accounts that have
   transactions but never incur a fee must still appear in the result with a fee of 0.

Key observations:
- Average amounts use absolute values even though balance calculations preserve deposit/withdrawal direction.
- Fee eligibility depends on chronological order, so transactions must be processed by timestamp rather than insertion order.
- Free-transaction counts are independent for each account, even when transactions from multiple accounts are interleaved.
- Initialize an account in the fee dictionary before skipping its free transactions so zero-fee accounts remain in the output.

Complexity:
- get_balance is O(n) time and O(1) extra space.
- get_average_transaction_amount_by_account is O(n) time and O(a) space for a accounts.
- get_transaction_fees is O(n log n) because the transactions are sorted by timestamp, with O(a) bookkeeping space in
  addition to the temporary sorted list.

Important edge cases include a missing account, exactly three transactions, multiple interleaved accounts, out-of-order input,
only deposits or only withdrawals, and negative input amounts when calculating absolute averages.
'''

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


@dataclass(frozen=True)
class Transaction:
    account_id: str
    transaction_type: TransactionType
    amount: float
    timestamp_sec: int


class TransactionManager:
    FREE_TRANSACTIONS_PER_ACCOUNT = 3
    DEPOSIT_FEE = 1.0
    WITHDRAWAL_FEE = 2.0

    def __init__(self) -> None:
        self.transactions: list[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def get_balance(self, account_id: str) -> float:
        balance = 0.0

        for transaction in self.transactions:
            if transaction.account_id != account_id:
                continue

            if transaction.transaction_type == TransactionType.DEPOSIT:
                balance += transaction.amount
            else:
                balance -= transaction.amount

        return balance

    def get_average_transaction_amount_by_account(self) -> dict[str, float]:
        totals: dict[str, float] = {}
        counts: dict[str, int] = {}

        for transaction in self.transactions:
            account_id = transaction.account_id
            totals[account_id] = totals.get(account_id, 0.0) + abs(transaction.amount)
            counts[account_id] = counts.get(account_id, 0) + 1

        return {
            account_id: totals[account_id] / counts[account_id]
            for account_id in totals
        }

    def get_transaction_fees(self) -> dict[str, float]:
        """Calculate fees chronologically and independently per account."""
        transaction_counts: dict[str, int] = {}
        fees: dict[str, float] = {}

        for transaction in sorted(
            self.transactions,
            key=lambda item: item.timestamp_sec,
        ):
            account_id = transaction.account_id
            fees.setdefault(account_id, 0.0)

            transaction_counts[account_id] = transaction_counts.get(account_id, 0) + 1
            if transaction_counts[account_id] <= self.FREE_TRANSACTIONS_PER_ACCOUNT:
                continue

            if transaction.transaction_type == TransactionType.DEPOSIT:
                fees[account_id] += self.DEPOSIT_FEE
            else:
                fees[account_id] += self.WITHDRAWAL_FEE

        return fees


def run_sample_tests() -> None:
    manager = TransactionManager()
    transactions = [
        Transaction("a", TransactionType.DEPOSIT, 100.0, 30),
        Transaction("a", TransactionType.WITHDRAWAL, 20.0, 10),
        Transaction("b", TransactionType.DEPOSIT, 50.0, 15),
        Transaction("a", TransactionType.DEPOSIT, 40.0, 20),
        Transaction("a", TransactionType.WITHDRAWAL, 10.0, 40),
        Transaction("a", TransactionType.DEPOSIT, 5.0, 50),
        Transaction("b", TransactionType.WITHDRAWAL, 5.0, 25),
    ]

    for transaction in transactions:
        manager.add_transaction(transaction)

    assert manager.get_balance("a") == 115.0
    assert manager.get_balance("missing") == 0.0

    averages = manager.get_average_transaction_amount_by_account()
    assert averages["a"] == 35.0
    assert averages["b"] == 27.5

    # Account a's chronological fourth and fifth transactions are charged.
    assert manager.get_transaction_fees() == {"a": 3.0, "b": 0.0}
    print("All transaction accounting sample tests passed.")


if __name__ == "__main__":
    run_sample_tests()

'''
Explanation:
1. get_balance applies direction based on TransactionType: deposits are added and withdrawals are subtracted.
2. get_average_transaction_amount_by_account uses two dictionaries, totals and counts, and adds abs(amount) for every
   transaction so the average represents transaction size rather than signed cash flow.
3. get_transaction_fees first sorts by timestamp_sec, then tracks how many transactions each account has seen. The first three
   are skipped, and each later transaction adds the fee associated with its type. fees.setdefault(account_id, 0.0) ensures an
   account with only free transactions is still returned with zero fees.

Summary:
- Separate signed balance logic from absolute transaction-size statistics.
- When a business rule depends on event order, process events chronologically.
- Maintain counters independently per account instead of using one global transaction count.
- Initialize result state before branches that may continue or skip processing.
'''
