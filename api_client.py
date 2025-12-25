import requests

BASE_API_URL: str = "http://89.125.92.143:8000"

def create_new_wallet():
    response: requests.Response = requests.post(f"{BASE_API_URL}/wallet/new")
    response.raise_for_status()
    return response.json()


def get_wallet_balance(address: str) -> int:
    response: requests.Response = requests.get(
        f"{BASE_API_URL}/balance/{address}"
    )
    response.raise_for_status()
    response_json = response.json()
    return int(response_json["balance"])


def send_new_transaction(receiver_address: str, transfer_amount: int, sender_private_key: str):
    payload = {
        "receiver": receiver_address,
        "amount": transfer_amount,
        "private_key": sender_private_key,
    }

    response: requests.Response = requests.post(
        f"{BASE_API_URL}/transaction/new",
        json=payload,
    )
    response.raise_for_status()
    return response.json()


def get_pending_transactions():
    response: requests.Response = requests.get(
        f"{BASE_API_URL}/pending"
    )
    response.raise_for_status()
    return response.json()


def mine_new_block(miner_address: str):
    payload = {"miner_address": miner_address}

    response: requests.Response = requests.post(
        f"{BASE_API_URL}/mine",
        json=payload,
    )
    response.raise_for_status()
    return response.json()
