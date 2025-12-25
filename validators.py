def validate_transaction(transfer_amount: int, sender_balance: int) -> None:
    if transfer_amount <= 0:
        raise ValueError("Сумма перевода должна быть больше нуля")

    if transfer_amount > sender_balance:
        raise ValueError("Недостаточно средств для выполнения транзакции")
