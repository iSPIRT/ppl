import itertools


class WalletProvider:
    """Wallet providers are commercial or private operators of a collection of wallets"""
    next_id = itertools.count().__next__

    def __init__(self, provider_id: int, handle: str):
        self.id = provider_id
        self.handle = handle
        self.wallets = {}

    def register_wallet(self, wallet):
        self.wallets[wallet.id] = wallet

    def get_wallet_for_id(self, wallet_id: int):
        return self.wallets[wallet_id]
