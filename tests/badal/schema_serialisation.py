import json
import unittest

from badal.journal.decoder import SchemaDecoder
from badal.journal.encoder import JournalType
from badal.notaries.notary_base import Notary
from badal.schema.attribute_types.detail_types import PublicIdType, AmountType, NotesType
from badal.schema.contracts import solidity_one_oh
from badal.schema.enums import Visibility
from badal.schema.model import Schema
from badal.schema.proofs import zokrates_one_oh
from badal.schema.states import StateType
from badal.schema.transactions import TransactionType


def get_cbdc_spec():
    spec_cbdc = Schema("ispirt.org/rbi_cbdc/spec", "RBI CBDC Schema", "0.1", solidity_one_oh,
                       zokrates_one_oh)
    cbdc_state_type = StateType("cbdc")
    cbdc_state_type.add_attribute_type("_", "bearer", PublicIdType())
    cbdc_state_type.add_attribute_type("_", "amount", AmountType("cbdc_inr", precision=3))
    cbdc_state_type.add_attribute_type("_", "notes", NotesType(maxlen=128), visibility=Visibility.Public)

    spec_cbdc.add_state_type(cbdc_state_type)

    cbdc_transfer_type = TransactionType("transfer")
    cbdc_transfer_type.add_state_type("_", cbdc_state_type)
    spec_cbdc.add_transaction_type(cbdc_transfer_type)
    return spec_cbdc


class TestSchemaSerialisation(unittest.TestCase):
    def test_schema_serialisation(self):
        notary = Notary()
        spec_cbdc = get_cbdc_spec()
        proof_runtime = spec_cbdc.proof_model.get_proof_runtime()
        # Create Table cbdc
        #    column id StateId
        #    column from PublicId
        #    column to PublicId
        #    column amount Amount
        #    public column notes Notes

        # Create Table Transfers
        #   column transaction_id TransactionId
        #
        # Create Table TransferStates
        #   column transaction_id TransactionId (refers to Transfers.transaction_id)
        #   column state_type StateTypeId (in this case this value will be "cbdc")
        #   column state_id StateId (refers to a state's id, in this particular case Cbdc.state_id
        #   column activity StateActivityEnum(will either be created or canceled .. only two possible values)

        #  cbdc record (state_id=1111 from="rbi" to="danny" amount=500.000)

        # transfers record (transaction_id=123)
        # transfer_states (transaction_id=123, state_type="cbdc" state_id=1111, activity="canceled")
        # transfer_states (transaction_id=123, state_type="cbdc", state_id=1112, activity="created")
        # transfer_states (transaction_id=123, state_type="cbdc", state_id=1113, activity="created")

        # cbdc record (state_id=1112 from="rbi" to="navin" amount=300.00)
        # cbdc record (state_id=1113 from="rbi" to="danny" amount=200.00)

        cbdc_json_dict = spec_cbdc.to_journal_dict(JournalType.Private, proof_runtime)
        cbdc_json_str = notary.notarise(spec_cbdc, JournalType.Private, proof_runtime)
        print(cbdc_json_str)
        cbdc_decoded = json.loads(cbdc_json_str, cls=SchemaDecoder)
        self.maxDiff = None
        self.assertDictEqual(cbdc_json_dict, cbdc_decoded)
