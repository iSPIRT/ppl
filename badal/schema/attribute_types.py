import enum
from typing import Dict, Any

from badal.journal.encoder import JournalEncodeable


class Visibility(enum.Enum):
    Private = "prv"
    Public = "pub"


class AttributeType(JournalEncodeable):
    def __init__(self, id: str, name: str, visibility: Visibility = Visibility.Private):
        self.id = id
        self.name = name
        self.visibility = visibility

    def to_reference_dict(self):
        raise NotImplementedError("not implemented")


class DecimalType(AttributeType):
    def to_reference_dict(self):
        return {
            "type": "decimal",
        }


class WalletType(AttributeType):
    def to_reference_dict(self):
        return {
            "type": "wallet",
        }


class DatetimeType(AttributeType):
    def to_reference_dict(self):
        return {
            "type": "datetime",
        }


class PublicIdType(AttributeType):
    def __init__(self):
        super(PublicIdType, self).__init__("http://ispirt.org/pplspecs/core/idtypes/publicid", "publicid", "Public Id")

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "visibility": self.visibility,
            "type": "public_id"
        }


class AmountType(AttributeType):
    def __init__(self, uom: str, precision: int = 15):
        super(AmountType, self).__init__("http://ispirt.org/pplspecs/core/idtypes/amount", "amount", "Amount")
        self.precision = precision
        self.uom = uom

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "visibility": self.visibility,
            "type": "amount",
            "precision": self.precision,
            "uom": self.uom
        }


class NotesType(AttributeType):
    def __init__(self, maxlen: int = 256):
        super(NotesType, self).__init__("http://ispirt.org/pplspecs/core/idtypes/notes", "notes", "Notes")
        self.maxlen = maxlen

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "visibility": self.visibility,
            "type": "notes"
        }
