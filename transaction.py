class Transaction:
    receiver_address: str
    transfer_amount: int

    def __init__(self, receiver_address: str, transfer_amount: int) -> None:
        self.receiver_address = receiver_address
        self.transfer_amount = transfer_amount
