from Crypto.Hash import SHA256


class Transaction:
    def __init__(self, t_type, receiver, amount, sender=None):
        self.t_type = t_type
        self.receiver = receiver
        self.amount = amount
        self.sender = sender

    def show(self):
        if self.t_type == "createCoins":
            return f"{self.amount} ==> {self.receiver}"
        elif self.t_type == "unspent":
            return f"{self.amount} --> {self.receiver}"
        else:
            return f"{self.sender} ==> {self.receiver} ({self.amount})"

    def get_hash(self):
        if self.t_type != "payCoins":
            return SHA256.new(
                bytes(f"{self.receiver}{self.amount}", "utf-8")
            ).hexdigest()
        else:
            return SHA256.new(
                bytes(f"{self.sender}{self.receiver}{self.amount}", "utf-8")
            ).hexdigest()
