import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256
import base64

# from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme


class Wallet:
    def __init__(self, name):
        self.name = name
        random_gen = Random.new().read
        private_key = RSA.generate(1024, random_gen)
        public_key = private_key.publickey()
        self.private_key = bytes.hex(private_key.exportKey(format="DER"))
        self.public_key = bytes.hex(public_key.exportKey(format="DER"))
        self.public_key_hash = SHA256.new(bytes(self.public_key, "utf-8")).hexdigest()


# signer = PKCS115_SigScheme(RSA.importKey(binascii.unhexlify(self.private_key)))
# signature = signer.sign(SHA256.new(b'hello'))
# verifier = PKCS115_SigScheme(RSA.importKey(binascii.unhexlify(self.public_key)))
# try:
#   verifier.verify(SHA256.new(b'hello'), signature)
#   print("Signature is valid.")
# except:
#   print("Signature is invalid.")
