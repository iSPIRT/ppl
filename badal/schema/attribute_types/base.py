import abc
from typing import Dict, Any, List

from badal.errors.Invalidity import Invalidity
from badal.journal.encoder import JournalEncodeable
from badal.schema.enums import Visibility


class AttributeType(JournalEncodeable, abc.ABC):
    registry: Dict[str, "AttributeType"] = {}

    @classmethod
    def register(cls, attr_type: "AttributeType"):
        cls.registry[attr_type.id] = attr_type

    @classmethod
    def get(cls, attr_id: str) -> "Optional[AttributeType]":
        cls.registry.get(attr_id)

    def __init__(self, id: str, name: str, visibility: Visibility, required: bool):
        self.id = id
        self.name = name
        self.visibility = visibility
        self.required = required

    @abc.abstractmethod
    def validate(self, value: Any) -> List[Invalidity]:
        []

    def to_journal_dict(self) -> Dict[str, Any]:
        raise NotImplementedError("not implemented")
