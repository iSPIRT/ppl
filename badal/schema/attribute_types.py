import abc
import enum
from typing import Dict, Any, List

from badal.errors.Invalidity import Invalidity
from badal.journal.encoder import JournalEncodeable


class Visibility(enum.Enum):
    Private = "prv"
    Public = "pub"


class AttributeType(JournalEncodeable, abc.ABC):
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    @abc.abstractmethod
    def validate(self, value: Any) -> List[Invalidity]:
        []

    def to_journal_dict(self) -> Dict[str, Any]:
        raise NotImplementedError("not implemented")


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

    def validate(self, value: Any) -> List[Invalidity]:
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

    def validate(self, value: Any) -> List[Invalidity]:
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

    def validate(self, value: Any) -> List[Invalidity]:
        if len(value) <= self.maxlen :
            return []
        else:
            return [Invalidity("err-value-too-long", { "actual-length": len(value), "max-length": self.maxlen})]


    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": "notes"
        }
