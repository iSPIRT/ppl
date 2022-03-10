import unittest

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey

from badal.notaries.notary_base import Notary
from badal.runtime.states import State, create_state
from badal.runtime.transactions import Transaction
from tests.badal.schema_serialisation import get_cbdc_spec


def generate_keypair() -> RsaKey:
    return RSA.generate(2048)


class TestTransactionNotarisation(unittest.TestCase):
    def test_transaction_notarisation(self):
        rbi_keypair = generate_keypair()
        rbi_public = rbi_keypair.publickey()
        cbdc_spec = get_cbdc_spec()
        transaction_type = cbdc_spec.transaction_types["transfer"]
        state_type = cbdc_spec.state_types["cbdc"]
        new_money_state = create_state(state_type, {
            "bearer": rbi_public,
            "amount": 500.00,
            "notes": "Initial Money Generation"
        })
        new_money = Transaction(transaction_type, [], [new_money_state])
        notary = Notary()
        notary.notarise_transaction(new_money)


