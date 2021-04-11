import pytest

from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


def test_transaction():
    sender_wallet = Wallet()
    recipient = 'recipient'
    amount = 50
    transaction = Transaction(sender_wallet, recipient, amount)

    assert transaction.output[recipient] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount

    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == sender_wallet.balance
    assert transaction.input['address'] == sender_wallet.address
    assert transaction.input['public_key'] == sender_wallet.public_key
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )


def test_transaction_exceeds_balance():
    with pytest.raises(Exception, match='Amount exceeds balance'):
        Transaction(Wallet(), 'recipient', 5000)


def test_transaction_update():
    sender_wallet = Wallet()
    first_recipient = 'first_recipient'
    first_recipient_amount = 25
    transaction = Transaction(sender_wallet, first_recipient, first_recipient_amount)

    second_recipient = 'second_recipient'
    second_recipient_amount = 50
    transaction.update(sender_wallet, second_recipient, second_recipient_amount)

    assert transaction.output[second_recipient] == second_recipient_amount
    assert transaction.output[sender_wallet.address] == \
           sender_wallet.balance - first_recipient_amount - second_recipient_amount
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

    first_recipient_second_amount = 125
    transaction.update(sender_wallet, first_recipient, first_recipient_second_amount)

    assert transaction.output[first_recipient] == \
           first_recipient_amount + first_recipient_second_amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance \
           - first_recipient_amount - second_recipient_amount - first_recipient_second_amount

    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )








def test_transaction_update_exceeds_balance():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 25)

    with pytest.raises(Exception, match='Amount exceeds balance'):
        Transaction(sender_wallet, 'recipient', 5000)

    with pytest.raises(Exception, match='Amount exceeds balance'):
        Transaction(sender_wallet, 'recipient_2', 5000)











