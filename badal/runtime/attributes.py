import decimal

from Crypto.PublicKey.RSA import RsaKey

from badal.journal.values import JournalEncodeableValue
from badal.schema.enums import Visibility
from badal.schema.states import AttributeDetails
from badal.utils.keys import key_to_hex


class PublicKeyAttributeValue(JournalEncodeableValue):
    def __init__(self, key: RsaKey):
        self.key = key

    def to_journal_value(self, attr_details: AttributeDetails) -> str:
        if attr_details.visibility == Visibility.Public :
            return key_to_hex(self.key)
        else :
            return f"Private equivalent of {key_to_hex(self.key)}"


class AmountAttributeValue(JournalEncodeableValue):
    def __init__(self, amount: decimal.Decimal):
        self.amount = amount

    def to_journal_value(self, attr_details: AttributeDetails) -> str:
        if attr_details.visibility == Visibility.Public :
            return str(self.amount)
        else :
            return f"Private equivalent of {self.amount}"


class NotesAttributeValue(JournalEncodeableValue):
    def __init__(self, text: str):
        self.text = text

    def to_journal_value(self, attr_details: AttributeDetails) -> str:
        return self.text