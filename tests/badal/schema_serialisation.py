import unittest
import json

from badal.journal.decoder import SchemaDecoder
from badal.notaries.notary_base import Notary
from badal.schema.attribute_types import PublicIdType, AmountType, NotesType, Visibility
from badal.schema.contracts import solidity_one_oh
from badal.schema.model import Specification
from badal.schema.proofs import zokrates_one_oh
from badal.schema.states import StateType
from badal.schema.transactions import TransactionType


class TestSchemaSerialisation(unittest.TestCase):
    def test_schema_serialisation(self):
        notary = Notary()
        spec_cbdc = Specification("http://ispirt.org/rbi_cbdc/spec", "RBI CBDC Schema", "0.1", solidity_one_oh,
                                  zokrates_one_oh)
        cbdc_state_type = StateType("cbdc")
        cbdc_state_type.add_attribute_type("_", "from", PublicIdType())
        cbdc_state_type.add_attribute_type("_", "to", PublicIdType())
        cbdc_state_type.add_attribute_type("_", "amount", AmountType("cbdc_inr", precision=3))
        cbdc_state_type.add_attribute_type("_", "notes", NotesType(maxlen=128), visibility=Visibility.Public)

        spec_cbdc.add_state_type(cbdc_state_type)

        cbdc_transfer_type = TransactionType("transfer")
        cbdc_transfer_type.add_state_type("_", cbdc_state_type)

        spec_cbdc.add_transaction_type(cbdc_transfer_type)
        cbdc_json_dict = spec_cbdc.to_journal_dict()
        cbdc_json_str = notary.notarise(spec_cbdc)
        cbdc_decoded = json.loads(cbdc_json_str, cls=SchemaDecoder)
        self.assertDictEqual(cbdc_json_dict, cbdc_decoded)