import decimal
from typing import List, Dict, Any

from Crypto.PublicKey.RSA import RsaKey

from badal.errors.Invalidity import Invalidity
from badal.journal.encoder import JournalType
from badal.journal.values import JournalEncodeableValue
from badal.schema.enums import Visibility
from badal.schema.proofs import ProofModel
from badal.schema.states import AttributeDetails
from badal.utils.keys import key_to_hex


class PublicKeyAttributeValue(JournalEncodeableValue):
    def __init__(self, key: RsaKey):
        self.key = key

    def to_journal_value(self, attr_details: AttributeDetails, journal_type: JournalType, proof_model: ProofModel) -> str:
        if attr_details.visibility == Visibility.Public or journal_type == JournalType.Private:
            return key_to_hex(self.key)
        else :
            return proof_model.hash(self.key.export_key(format="DER"))

    def validate(self, type: Dict[str, Any]) -> List[Invalidity]:
        return []


class AmountAttributeValue(JournalEncodeableValue):
    def __init__(self, amount: decimal.Decimal):
        self.amount = amount

    def to_journal_value(self, attr_details: AttributeDetails, journal_type: JournalType, proof_model: ProofModel) -> str:
        if attr_details.visibility == Visibility.Public or journal_type == JournalType.Private:
            return str(self.amount)
        else :
            return proof_model.hash(str(self.amount).encode('utf-8'))

    def validate(self, type: Dict[str, Any]) -> List[Invalidity]:
        return []


class NotesAttributeValue(JournalEncodeableValue):
    def __init__(self, text: str):
        self.text = text

    def to_journal_value(self, attr_details: AttributeDetails, journal_type: JournalType, proof_model: ProofModel) -> str:
        if attr_details.visibility == Visibility.Public or journal_type == JournalType.Private:
            return self.text
        else:
            return proof_model.hash(self.text.encode('utf-8'))

    def validate(self, type: Dict[str, Any]) -> List[Invalidity]:
        return []
