from Crypto.Hash import SHA256

h = SHA256.new()


class Block:
    def __init__(self, block_no, transactions, prev_block_hash):
        self.id = block_no
        self.transactions = transactions.copy()
        self.prev_block_hash = prev_block_hash
        self.merkle_root_hash = self.generate_merkle_root_hash(transactions)
        self.block_hash, self.nonce = self.get_block_hash()

    def generate_merkle_root_hash(self, transactions):

        for i in range(len(transactions)):
            transactions[i] = transactions[i].get_hash()

        if len(transactions) == 2:
            a = transactions.pop()
            b = transactions.pop()
            h.update(bytes(a + b, "utf-8"))
            return h.hexdigest()
        else:
            return transactions.pop()

    def get_block_hash(self):
        nonce = 0
        while True:
            h.update(
                bytes(
                    str(nonce) + str(id) + self.merkle_root_hash + self.prev_block_hash,
                    "utf-8",
                )
            )
            if h.hexdigest()[0] == "0":
                return h.hexdigest(), nonce
            nonce += 1
        return "0" * 64, 0
