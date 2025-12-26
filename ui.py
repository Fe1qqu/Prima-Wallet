import tkinter as tk
from tkinter import messagebox
from typing import Optional

from api_client import (
    create_new_wallet,
    get_wallet_balance,
    send_new_transaction,
    get_pending_transactions,
    mine_new_block,
)
from wallet import Wallet
from validators import validate_transaction

class WalletApplication:
    root_window: tk.Tk
    wallet: Optional[Wallet]

    address_label: tk.Label
    balance_label: tk.Label

    receiver_address_entry: tk.Entry
    transfer_amount_entry: tk.Entry

    def __init__(self, root_window: tk.Tk) -> None:
        self.root_window = root_window
        self.root_window.title("PrimaCoin Wallet")

        self.wallet = Wallet.load_from_file()

        self.address_label = tk.Label(root_window, text="Адрес: —")
        self.address_label.pack()

        self.balance_label = tk.Label(root_window, text="Баланс: —")
        self.balance_label.pack()

        tk.Button(
            root_window,
            text="Создать кошелёк",
            command=self.create_wallet,
        ).pack()

        tk.Button(
            root_window,
            text="Обновить баланс",
            command=self.update_balance,
        ).pack()

        tk.Label(root_window, text="Адрес получателя").pack()
        self.receiver_address_entry = tk.Entry(root_window, width=40)
        self.receiver_address_entry.pack()

        tk.Label(root_window, text="Сумма перевода").pack()

        vcmd = (root_window.register(self.only_digits), "%P")

        self.transfer_amount_entry = tk.Entry(
            root_window,
            validate="key",
            validatecommand=vcmd
        )
        self.transfer_amount_entry.pack()

        tk.Button(
            root_window,
            text="Отправить транзакцию",
            command=self.send_transaction,
        ).pack()

        tk.Button(
            root_window,
            text="Показать необработанные транзакции",
            command=self.show_pending_transactions,
        ).pack()

        tk.Button(
            root_window,
            text="Майнить блок",
            command=self.mine_block,
        ).pack()

        self.refresh_interface()

    def refresh_interface(self) -> None:
        if self.wallet is not None:
            self.address_label.config(text=f"Адрес: {self.wallet.address}")
            self.update_balance()

    def create_wallet(self) -> None:
        wallet_data = create_new_wallet()

        self.wallet = Wallet(
            address=wallet_data["address"],
            public_key=wallet_data["public_key"],
            private_key=wallet_data["private_key"],
        )
        self.wallet.save_to_file()
        self.refresh_interface()

        warning_text: str = wallet_data.get("warning", "")

        messagebox.showinfo("Кошелёк создан", f"Сохраните private key!\n{warning_text}")

    def update_balance(self) -> None:
        if self.wallet is None:
            return

        balance: int = get_wallet_balance(self.wallet.address)
        self.balance_label.config(text=f"Баланс: {balance}")

    def send_transaction(self) -> None:
        if self.wallet is None:
            messagebox.showerror("Ошибка", "Кошелёк не создан")
            return

        receiver_address: str = self.receiver_address_entry.get()
        if not self.transfer_amount_entry.get():
            messagebox.showerror("Ошибка", "Введите сумму перевода")
            return
        transfer_amount: int = int(self.transfer_amount_entry.get())

        sender_balance: int = get_wallet_balance(self.wallet.address)

        try:
            validate_transaction(transfer_amount, sender_balance)
        except ValueError as error:
            messagebox.showerror("Ошибка", str(error))
            return

        send_new_transaction(
            receiver_address,
            transfer_amount,
            self.wallet.private_key,
        )

        messagebox.showinfo("Успех", "Транзакция успешно отправлена")
        self.update_balance()

    def show_pending_transactions(self) -> None:
        pending_transactions = get_pending_transactions()
        messagebox.showinfo("Необработанные транзакции", str(pending_transactions))

    def mine_block(self) -> None:
        if self.wallet is None:
            return

        mining_result = mine_new_block(self.wallet.address)
        messagebox.showinfo("Майнинг", str(mining_result))
        self.update_balance()

    def only_digits(self, new_value: str) -> bool:
        return new_value.isdigit() or new_value == ""

if __name__ == "__main__":
    root = tk.Tk()
    application = WalletApplication(root)
    root.mainloop()
