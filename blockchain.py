import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256
import base64
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme


class Blockchain:
    def __init__(self):
        self.chain = []

    def create_block(self, block):
        self.chain.append(block)

    def print_center(self, string):
        print("|", end="")
        print(string.center(38), end="")
        print("|")

    def display(self):
        for block in self.chain:
            print("-" * 40)
            self.print_center(f"Block No. {block.id}")
            print("-" * 40)
            self.print_center(f"Nonce: {block.nonce}")
            print("-" * 40)
            for t in block.transactions:
                if t.t_type == "unspent":
                    self.print_center("Unspent Transaction:")
                    self.print_center(t.show())
                else:
                    self.print_center("Transaction:")
                    self.print_center(t.show())

            print("-" * 40)
            self.print_center("Previous Block Hash:")
            self.print_center(block.prev_block_hash[0:32])
            self.print_center(block.prev_block_hash[32:64])
            print("-" * 40)
            self.print_center("Block Hash:")
            self.print_center(block.block_hash[0:32])
            self.print_center(block.block_hash[32:64])
            print("-" * 40)

    def size(self):
        return len(self.chain)

    def sign_transaction(self, private_key, transaction_hash):
        signer = PKCS115_SigScheme(RSA.importKey(bytes.fromhex(private_key)))
        signature = signer.sign(SHA256.new(bytes(transaction_hash, "utf-8")))
        return signature

    def validate_transaction(self, signature, public_key, transaction_hash):
        verifier = PKCS115_SigScheme(RSA.importKey(bytes.fromhex(public_key)))
        try:
            verifier.verify(SHA256.new(bytes(transaction_hash, "utf-8")), signature)
        except:
            return False
        return True
