import os
import glob
from wallet import Wallet
from transaction import Transaction
from block import Block
from blockchain import Blockchain


class Currency:
    def __init__(self):
        self.blockchain = Blockchain()
        self.wallets = {}
        self.utxo_database = {}

    def validate_signature(self, username, t_hash):
        key = input("Enter private key: ")
        try:
            signature = self.blockchain.sign_transaction(key, t_hash)
        except:
            return False
        return self.blockchain.validate_transaction(
            signature, self.wallets[username].public_key, t_hash
        )

    def validate_double_spending(self, username, amount):
        return sum(self.utxo_database[self.wallets[username].public_key_hash]) >= amount

    def generate_wallet(self, username):
        w = Wallet(username)
        self.wallets[username] = w
        self.utxo_database[w.public_key_hash] = []
        # Save private key of user in a folder
        f = open(f"./secrets/{username}_private_key.txt", "w+")
        f.write(w.private_key)
        f.close()

    def print_utxo_database(self):
        print()
        for key in self.utxo_database:
            print(f"{key} ->     ", end=" ")

            for utxo in self.utxo_database[key]:
                print(utxo, end=" ,  ")
            print()

    def create_coins(self, user_name, amount):
        t = Transaction("createCoins", user_name, amount)

        is_valid = self.validate_signature(user_name, t.get_hash())

        if is_valid:
            if self.blockchain.size() == 0:
                block = Block(self.blockchain.size(), [t], "0" * 64)  # Genesis Block
            else:
                block = Block(
                    self.blockchain.size(),
                    [t],
                    self.blockchain.chain[-1].block_hash,
                )
            self.utxo_database[self.wallets[user_name].public_key_hash].append(amount)
            self.blockchain.create_block(block)
            print("\nBlock created!!")
        else:
            print("\nInvalid signature!!")

    def send_coins(self, sender_name, reciever_name, amount):
        validate = self.validate_double_spending(sender_name, amount)
        if validate:

            amt = 0
            i = 0
            while amt < amount:
                amt += self.utxo_database[self.wallets[sender_name].public_key_hash][i]
                i += 1

            t1 = Transaction("payCoins", reciever_name, amount, sender_name)
            t2 = Transaction("unspent", sender_name, amt - amount)
            is_valid = self.validate_signature(
                sender_name, t1.get_hash() + t2.get_hash()
            )

            if is_valid:
                amt = 0
                while amt < amount:
                    amt += self.utxo_database[
                        self.wallets[sender_name].public_key_hash
                    ].pop(0)

                if self.blockchain.size() == 0:
                    block = Block(
                        self.blockchain.size(), [t1, t2], "0" * 64
                    )  # Genesis Block
                else:
                    block = Block(
                        self.blockchain.size(),
                        [t1, t2],
                        self.blockchain.chain[-1].block_hash,
                    )
                self.utxo_database[self.wallets[sender_name].public_key_hash].append(
                    amt - amount
                )
                self.utxo_database[self.wallets[reciever_name].public_key_hash].append(
                    amount
                )
                self.blockchain.create_block(block)
                print("\nBlock created!!")
            else:
                print("\nInvalid signature!!")
        else:
            print("\nDouble spending detected!!")

    def simulation(self):
        while True:
            choice = int(
                input(
                    "\n\n1. Create wallet\n2. Perform Transaction\n3. Visualize Blockchain\n4. Visualize UTXO database\n5. END\n"
                )
            )

            if choice == 1:
                username = input("\nEnter user name: ")
                self.generate_wallet(username)

            elif choice == 2:
                t_type = int(
                    input("\nSelect transaction type\n1. Create coins\n2. Pay coins\n")
                )

                if t_type == 1:
                    username = input("\nEnter user name: ")
                    amount = int(input("Enter amount: "))
                    self.create_coins(username, amount)

                else:
                    sender_name = input("Enter sender name: ")
                    reciever_name = input("Enter receiver name: ")
                    amount = int(input("Enter amount: "))
                    self.send_coins(sender_name, reciever_name, amount)

            elif choice == 3:
                self.blockchain.display()

            elif choice == 4:
                self.print_utxo_database()

            else:
                # Delete all private keys
                files = glob.glob("./keys/*.txt")
                for f in files:
                    os.remove(f)
                break
