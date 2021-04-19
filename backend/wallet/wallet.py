import json
import uuid

from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature
)


class Wallet:
    def __init__(self):
        self.address = str(uuid.uuid4())[0:8]
        self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(),
            default_backend())
        self.public_key = self.private_key.public_key()
        self.serialize_public_key()

    def sign(self, data):
        return decode_dss_signature(
            self.private_key.sign(
            json.dumps(data).encode('utf-8'),
            ec.ECDSA(hashes.SHA256())))

    def serialize_public_key(self):
        self.public_key = self.public_key.public_bytes(
            encoding = serialization.Encoding.PEM,
            format = serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

    @staticmethod
    def verify(public_key, data, signature):
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )

        (r, s) = signature
        try:
            deserialized_public_key.verify(
                encode_dss_signature(r, s),
                json.dumps(data).encode('utf-8'),
                ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False


def main():
    wallet = Wallet()
    print(f'wallet.__dict__ : {wallet.__dict__}')

    data = {'foo':'boo'}
    tempered_data = 'tempered_block'
    signature = wallet.sign(data)
    print(f'signature : {signature}')

    signature_should_be_verified = Wallet.verify(wallet.public_key, data, signature)
    print(f'signature_should_be_verified: {signature_should_be_verified}')

    signature_should_be_invalid = Wallet.verify(Wallet().public_key, data, signature)
    print(f'signature_should_be_invalid: {signature_should_be_invalid}')

    signature_should_be_invalid = Wallet.verify(Wallet().public_key, tempered_data, signature)
    print(f'signature_should_be_invalid: {signature_should_be_invalid}')


if __name__ == '__main__':
    main()
