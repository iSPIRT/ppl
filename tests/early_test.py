import json
import logging.config
import unittest

from dinero.types.ecosystem import Ecosystem
from dinero.types.notary import Notary
from dinero.types.public_journal import PublicJournal
from dinero.types.state import State, deserialise_state
from dinero.types.transaction import Transaction
from dinero.types.value_store import UOM
from dinero.types.wallet import Wallet
from dinero.types.wallet_provider import WalletProvider
from dinero.utils.customjson import DineroEncoder

logging.config.fileConfig('../logging.conf')
from decimal import Decimal

from dinero.types.walletjournal import WalletJournal

from dinero.types.entity import CentralBank
from dinero.types.iou import IOU, IOUType

log = logging.getLogger("Dinero")


class Dinero(unittest.TestCase):
    def test_currency_serialisation(self):
        ecosystem = Ecosystem()

        # Create Notary
        mi = Notary("MI", ecosystem)
        ecosystem.add_notary(mi)

        # Create Wallet Provider for Central Bank
        cwp = WalletProvider(WalletProvider.next_id(), "CWP")
        ecosystem.add_wallet_provider(cwp)

        # Create Central Bank
        cb = CentralBank(ecosystem, "RBI", cwp)

        # Create issuance of one lakh Rs.
        one_lakh_issuance = IOU(State.next_id(), IOUType.Currency, cb.main_wallet, cb.main_wallet, UOM.Currency_INR, Decimal("100000.00"))

        # aside .. testing currency serialisation
        log.debug("Serialising currency object {}".format(one_lakh_issuance))
        serialised = json.dumps(one_lakh_issuance.serialise().to_json(), cls=DineroEncoder)
        data = json.loads(serialised)
        deserialised_state = deserialise_state(ecosystem, data)
        log.debug("Deserialised currency object {}".format(deserialised_state))
        self.assertEqual(one_lakh_issuance, deserialised_state,
                         "Serialised currency object is not the same as deserialised currency")

        created_states = [one_lakh_issuance]
        transaction = Transaction(None, created_states, "RBI issues one lakh \u20b9.")
        mi.record(transaction)


if __name__ == '__main__':
    unittest.main()
