from backend.wallet.wallet import Wallet


def test_verify_valid_sinature():
    data = {'foo': 'test_data'}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert Wallet.verify(wallet.public_key, data, signature)


def test_verify_invalid_sinature():
    data = {'foo': 'test_data'}
    tempered_data = 'tempered_block'
    wallet = Wallet()
    signature = wallet.sign(data)

    assert not Wallet.verify(Wallet().public_key, data, signature)
    assert not Wallet.verify(Wallet().public_key, tempered_data, signature)
    assert not Wallet.verify(Wallet().public_key, tempered_data, Wallet().sign(data))