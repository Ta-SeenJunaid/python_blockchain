import time
import uuid

from backend.wallet.wallet import Wallet


class Transaction:

    def __init__(self, sender_wallet, recipient, amount):

        self.id = str(uuid.uuid4())[0:8]
        self.output = self.create_output(sender_wallet,
                                         recipient,
                                         amount)
        self.input = self.create_input(sender_wallet, self.output)

    @staticmethod
    def create_output(sender_wallet, recipient, amount):

        if amount > sender_wallet.balance:
            raise Exception('Amount exceeds balance')

        output = {
            recipient: amount,
            sender_wallet.address: sender_wallet.balance - amount}

        return output

    @staticmethod
    def create_input(sender_wallet, output):

        return {
            'timestamp': time.time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output)
        }


def main():
    transaction = Transaction(Wallet(), 'recipient', 25)
    print(f'transaction.__dict__ : {transaction.__dict__}')


if __name__ == '__main__':
    main()




