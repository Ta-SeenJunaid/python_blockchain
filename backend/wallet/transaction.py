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

    def update(self, sender_wallet, recipient, amount):

        if amount > self.output[sender_wallet.address]:
            raise Exception('Amount exceeds balance')

        if recipient in self.output:
            self.output[recipient] += amount
        else:
            self.output[recipient] = amount

        self.output[sender_wallet.address] -= amount
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

    @staticmethod
    def is_valid_transaction(transaction):
        output_total = sum(transaction.output.values())

        if transaction.input['amount'] != output_total:
            raise Exception('Invalid transaction output values')

        if not Wallet.verify(
            transaction.input['public_key'],
            transaction.output,
            transaction.input['signature']
        ):
            raise Exception('Invalid signature')


def main():
    wallet = Wallet()
    transaction = Transaction(wallet, 'recipient', 25)
    print(f'transaction.__dict__ : {transaction.__dict__}')

    transaction.update(wallet, 'recipient', 50)
    print(f'transaction.__dict__ : {transaction.__dict__}')

    transaction.update(wallet, 'recipient_2', 50)
    print(f'transaction.__dict__ : {transaction.__dict__}')


if __name__ == '__main__':
    main()




