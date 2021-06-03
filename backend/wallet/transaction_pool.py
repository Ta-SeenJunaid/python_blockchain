class TransactionPool:
    def __init__(self):
        self.transaction_map = {}

    def set_transaction(self, transaction):
        self.transaction_map[transaction.id] = transaction

    def existing_transaction(self, address):
        for transaction in self.transaction_map.values():
            if transaction.input['address'] == address:
                return transaction