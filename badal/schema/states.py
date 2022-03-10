import abc
from dataclasses import dataclass
from typing import Dict, Tuple, Any, List

from badal.errors.Invalidity import Invalidity
from badal.schema.attribute_types import AttributeType, Visibility
from badal.schema.types import SpecAddress, GlobalId
from badal.journal.encoder import JournalEncodeable


@dataclass
class AttributeDetails(JournalEncodeable):
    id: str
    type: AttributeType
    required: bool
    visibility: Visibility

    def validate(self, value: Any) -> List[Invalidity]:
        return self.type.validate(value)

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.to_journal_dict(),
            "required": self.required,
            "visibility": self.visibility
        }


class StateType(JournalEncodeable):
    def __init__(self, id: str):
        self.id = id
        self.attributes: Dict[GlobalId, AttributeDetails] = {}

    def add_attribute_type(self, spec: str, id: str, type: AttributeType, required: bool = True,
                           visibility: Visibility = Visibility.Private):
        self.attributes[GlobalId(spec=spec, id=id)] = AttributeDetails(id, type, required, visibility)

    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "attributes": {
    #             key: val.to_journal_dict() for key, val in self.attributes.items()
    #         },
    #     }

    # def to_reference_dict(self):
    #     return {
    #         "id": self.id,
    #         "attributes": {key: val.to_reference_dict() for key, val in self.attributes.items()},
    #     }

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "attributes": [{"key": k, "value": v.to_journal_dict()} for k, v in self.attributes.items()]
        }

    @classmethod
    def from_journal_dict(cls, dict: Dict[str, Any]) -> "StateType":
        return None


@dataclass
class StateDetails:
    spec: str
    state_type: str
    allow_cancel: bool
    allow_create: bool

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "spec": self.spec,
            "state_type": self.state_type,
            "allow_cancel": self.allow_cancel,
            "allow_create": self.allow_create
        }

    @classmethod
    def from_journal_dict(cls, dict: Dict[str, Any]) -> "StateDetails":
        return StateDetails(dict["spec"], dict["state_type"], dict["allow_cancel"], dict["allow_create"])
