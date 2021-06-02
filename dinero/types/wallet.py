import itertools

from dinero.types.wallet_provider import WalletProvider
from dinero.utils.crypto import generate_keypair


class Wallet:
    next = itertools.count().__next__

    def __init__(self, wallet_id: int, code: str):
        self.id = wallet_id
        self.code = code
        self.key = generate_keypair("w_{}_key".format(wallet_id))

    def __str__(self):
        return "W({}:{})".format(self.id, self.code)
