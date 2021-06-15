from ppl.types.notary import Notary
from ppl.types.public_journal import PublicJournal
from ppl.types.wallet import Wallet
from ppl.types.wallet_provider import WalletProvider


class Ecosystem:
    def __init__(self):
        self.notaries = {}
        self.wallet_providers = {}
        self.journal = PublicJournal()
        self.provider_map = {}

    def add_notary(self, notary: Notary):
        self.notaries[notary.id] = notary

    def add_wallet_provider(self, provider: WalletProvider):
        self.wallet_providers[provider.id] = provider

    def associate_wallet_to_provider(self, wallet: Wallet, provider: WalletProvider):
        self.provider_map[wallet.id] = provider

    def get_wallet_for_id(self, wallet_id):
        return self.provider_map[wallet_id].get_wallet_for_id(wallet_id)
