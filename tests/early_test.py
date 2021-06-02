import json
import logging.config
import unittest

from dinero.types.state import State, deserialise_state
from dinero.utils.customjson import DineroEncoder

logging.config.fileConfig('../logging.conf')
from decimal import Decimal

from dinero.types.journal import Journal


from dinero.types.entity import Entity, CentralBank
from dinero.types.iou import IOU, IOUType

log = logging.getLogger("Dinero")


class Dinero(unittest.TestCase):
    def test_currency_serialisation(self):
        cb_journal = Journal("CB")
        log.debug("Created central bank journal {}".format(cb_journal))
        cb = CentralBank("RBI", "RBI ONE", cb_journal)
        one_lakh_issuance_state = IOU(State.next_id(), IOUType.Currency, cb.main_wallet, cb.main_wallet, Decimal("100000.00"))
        log.debug("Serialising currency object {}".format(one_lakh_issuance_state))
        serialised = json.dumps(one_lakh_issuance_state.serialise().to_json(), cls=DineroEncoder)
        data = json.loads(serialised)
        deserialised_state = deserialise_state(data)
        log.debug("Deserialised currency object {}".format(deserialised_state))
        # Below still fails because references aren't fully resolved yet
        self.assertEqual(one_lakh_issuance_state, deserialised_state, "Serialised currency object is not the same as deserialised currency")


    def test_currency_issurance(self):
        # mi = Notary("MI")
        cb_journal = Journal("CB")
        log.debug("Created central bank journal {}".format(cb_journal))
        cb = CentralBank("RBI", "RBI ONE", cb_journal)
        one_lakh_issuance_state = IOU(State.next_id(), IOUType.Currency, cb.main_wallet, cb.main_wallet,
                                      Decimal("100000.00"))
        log.debug("Serialising currency object {}".format(one_lakh_issuance_state))
        serialised = json.dumps(one_lakh_issuance_state.serialise().to_json(), cls=DineroEncoder)
        data = json.loads(serialised)
        deserialised_state = deserialise_state(data)
        log.debug("Deserialised currency object {}".format(deserialised_state))
        # Below still fails because references aren't fully resolved yet
        self.assertEqual(one_lakh_issuance_state, deserialised_state,
                         "Serialised currency object is not the same as deserialised currency")
        # mi.create_state()
        # show_global_state()

if __name__ == '__main__':
    unittest.main()
