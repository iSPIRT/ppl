import logging

from dinero.utils.crypto import generate_keypair
from dinero.types.wallet import Wallet

log = logging.getLogger("Central Bank")


class Entity:
    """An entity is any legal person who participates in economic activity as a user of the system"""
    def __init__(self, code):
        self.code = code
        log.debug("Created entity {}".format(code))


class CentralBank(Entity):
    """A Central bank is a one off entity with special powers to issue currency"""
    def __init__(self, code, main_wallet_code, main_wallet_journal):
        super().__init__(code)
        self.key = generate_keypair('rbi_cur_key')
        self.main_wallet = Wallet(main_wallet_code, self.key, main_wallet_journal)
