import logging

from ppl.types.ecosystem import Ecosystem
from ppl.types.wallet_provider import WalletProvider
from ppl.utils.crypto import generate_keypair
from ppl.types.wallet import Wallet

log = logging.getLogger("Central Bank")


class Entity:
    """An entity is any legal person who participates in economic activity as a user of the system"""
    def __init__(self, code):
        self.code = code
        log.debug("Created entity {}".format(code))


class CentralBank(Entity):
    """A Central bank is a one off entity with special powers to issue currency"""
    def __init__(self, ecosystem: Ecosystem, code: str, main_wallet_provider: WalletProvider):
        super().__init__(code)
        self.main_wallet = Wallet(Wallet.next(), "RBI ONE")
        self.key = generate_keypair('rbi_cur_key')
        self.provider = main_wallet_provider
        self.provider.register_wallet(self.main_wallet)
        ecosystem.associate_wallet_to_provider(self.main_wallet, self.provider)
