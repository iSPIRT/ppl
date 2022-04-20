import unittest

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey

from badal.journal.encoder import JournalType
from badal.notaries.notary_base import Notary
from badal.runtime.attributes import PublicKeyAttributeValue, AmountAttributeValue, NotesAttributeValue
from badal.runtime.states import create_state
from badal.runtime.transactions import create_transaction
from tests.badal.schema_serialisation import get_cbdc_spec


def generate_keypair() -> RsaKey:
    return RSA.generate(1024)


class TestTransactionNotarisation(unittest.TestCase):
    def test_transaction_notarisation(self):
        rbi_keypair = generate_keypair()
        rbi_public = rbi_keypair.publickey()
        recipient_keypair = generate_keypair()
        cbdc_spec = get_cbdc_spec()
        proof_runtime = cbdc_spec.proof_model.get_proof_runtime()

        transaction_type = cbdc_spec.transaction_types["transfer"]
        state_type = cbdc_spec.state_types["cbdc"]

        new_money_state = create_state(state_type, {
            "bearer": PublicKeyAttributeValue(rbi_public),
            "amount": AmountAttributeValue(500.00),
            "notes": NotesAttributeValue("Initial Money Generation")
        })

        new_money = create_transaction(transaction_type, [], [new_money_state])
        new_money.sign(rbi_keypair, JournalType.Public, proof_runtime)
        new_money.sign(recipient_keypair, JournalType.Public, proof_runtime)
        # new_money.to_journal_dict()
        notary = Notary()
        notary.notarise_transaction(new_money, JournalType.Public, proof_runtime)
