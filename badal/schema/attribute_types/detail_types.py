from typing import Dict, Any, List

from badal.errors.Invalidity import Invalidity
from badal.runtime.attributes import AmountAttributeValue, PublicKeyAttributeValue, NotesAttributeValue
from badal.schema.attribute_types.base import AttributeType


class DecimalType(AttributeType):
    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "type": "decimal",
        }




class WalletType(AttributeType):
    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "type": "wallet",
        }




class DatetimeType(AttributeType):
    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "type": "datetime",
        }




class PublicIdType(AttributeType):
    def __init__(self):
        super(PublicIdType, self).__init__("publicid", "Public Id")

    def validate(self, value: PublicKeyAttributeValue) -> List[Invalidity]:
        return []

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": "public_id"
        }




class AmountType(AttributeType):
    def __init__(self, uom: str, precision: int = 15):
        super(AmountType, self).__init__("amount", "Amount")
        self.precision = precision
        self.uom = uom

    def validate(self, value: AmountAttributeValue) -> List[Invalidity]:
        return []

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": "amount",
            "precision": self.precision,
            "uom": self.uom
        }




class NotesType(AttributeType):
    def __init__(self, maxlen: int = 256):
        super(NotesType, self).__init__("notes", "Notes")
        self.maxlen = maxlen

    def validate(self, value: NotesAttributeValue) -> List[Invalidity]:
        if len(value.text) <= self.maxlen:
            return []
        else:
            return [Invalidity("err-value-too-long", {"actual-length": len(value.text), "max-length": self.maxlen})]

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": "notes"
        }


