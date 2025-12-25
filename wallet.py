import json
import os

class Wallet:
    FILE_NAME: str = "wallet.json"

    address: str
    public_key: str
    private_key: str

    def __init__(self, address: str, public_key: str, private_key: str) -> None:
        self.address = address
        self.public_key = public_key
        self.private_key = private_key

    def save_to_file(self) -> None:
        wallet_data = {
            "address": self.address,
            "public_key": self.public_key,
            "private_key": self.private_key,
        }

        with open(self.FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(wallet_data, file, indent=2, ensure_ascii=False)

    @classmethod
    def load_from_file(cls):
        if not os.path.exists(cls.FILE_NAME):
            return None

        try:
            with open(cls.FILE_NAME, "r", encoding="utf-8") as file:
                wallet_data = json.load(file)
        except json.JSONDecodeError:
            return None

        return cls(
            address=wallet_data["address"],
            public_key=wallet_data["public_key"],
            private_key=wallet_data["private_key"],
        )
