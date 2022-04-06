from typing import Dict, Any, List

from badal.errors.Invalidity import Invalidity
from badal.runtime.attributes import AmountAttributeValue, PublicKeyAttributeValue, NotesAttributeValue
from badal.schema.attribute_types.base import AttributeType
from badal.schema.enums import Visibility


class DecimalType(AttributeType):
    def __init__(self, visibility: Visibility = Visibility.Private, required: bool = True):
        super(PublicIdType, self).__init__("decimal", "Decimal", visibility, required)

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "type_id": self.id,
            "name": self.name,
            "type": "decimal",
            "visibility": self.visibility,
            "required": self.required,
        }

    def validate(self, value: Any) -> List[Invalidity]:
        return []


class WalletType(AttributeType):
    def __init__(self, visibility: Visibility = Visibility.Private, required: bool = True):
        super(PublicIdType, self).__init__("wallet_id", "Wallet ID", visibility, required)

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "type_id": self.id,
            "name": self.name,
            "type": "wallet",
            "visibility": self.visibility,
            "required": self.required,
        }

    def validate(self, value: Any) -> List[Invalidity]:
        return []


class DatetimeType(AttributeType):
    def __init__(self, visibility: Visibility = Visibility.Private, required: bool = True):
        super(PublicIdType, self).__init__("datetime", "Date Time", visibility, required)

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "type_id": self.id,
            "name": self.name,
            "type": "datetime",
            "visibility": self.visibility,
            "required": self.required,
        }

    def validate(self, value: Any) -> List[Invalidity]:
        return []


class PublicIdType(AttributeType):
    def __init__(self, visibility: Visibility = Visibility.Private, required: bool = True):
        super(PublicIdType, self).__init__("public_id", "Public Id", visibility, required)

    def validate(self, value: PublicKeyAttributeValue) -> List[Invalidity]:
        return []

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "type_id": self.id,
            "name": self.name,
            "type": "public_id",
            "visibility": self.visibility,
            "required": self.required,
        }

    def validate(self, value: Any) -> List[Invalidity]:
        return []


class AmountType(AttributeType):
    def __init__(self, uom: str, precision: int = 15, visibility: Visibility = Visibility.Private,
                 required: bool = True):
        super(AmountType, self).__init__("amount", "Amount", visibility, required)
        self.precision = precision
        self.uom = uom

    def validate(self, value: AmountAttributeValue) -> List[Invalidity]:
        return []

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "type_id": self.id,
            "name": self.name,
            "type": "amount",
            "visibility": self.visibility,
            "required": self.required,
            "precision": self.precision,
            "uom": self.uom,
        }


class NotesType(AttributeType):
    def __init__(self, maxlen: int = 256, visibility: Visibility = Visibility.Private, required: bool = True):
        super(NotesType, self).__init__("notes", "Notes", visibility, required)
        self.maxlen = maxlen

    def validate(self, value: NotesAttributeValue) -> List[Invalidity]:
        if len(value.text) <= self.maxlen:
            return []
        else:
            return [Invalidity("err-value-too-long", {"actual-length": len(value.text), "max-length": self.maxlen})]

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "type_id": self.id,
            "name": self.name,
            "type": "notes",
            "visibility": self.visibility,
            "required": self.required,
        }
