from dataclasses import dataclass
from typing import Dict, Tuple, Any

from badal.schema.attribute_types import AttributeType, Visibility
from badal.schema.types import SpecAddress, GlobalId
from badal.journal.encoder import JournalEncodeable


@dataclass
class AttributeDetails(JournalEncodeable):
    id: str
    type: AttributeType
    required: bool
    visibility: Visibility

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "required": self.required,
            "visibility": self.visibility
        }


class StateType(JournalEncodeable):
    def __init__(self, id: str):
        self.id = id
        self.attributes: Dict[Tuple[SpecAddress, str], AttributeDetails] = {}

    def add_attribute_type(self, spec: str, id: str, type: AttributeType, required: bool = True,
                           visibility: Visibility = Visibility.Private):
        self.attributes[GlobalId(spec=spec, id=id)] = AttributeDetails(id, type, required, visibility)

    def to_dict(self):
        return {
            "id": self.id,
            "attributes": {
                key: val.to_dict() for key, val in self.attributes.items()
            },
        }

    def to_reference_dict(self):
        return {
            "id": self.id,
            "attributes": {key: val.to_reference_dict() for key, val in self.attributes.items()},
        }

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "attributes": [{"key": k, "value": v} for k, v in self.attributes.items()]
        }


@dataclass
class StateDetails:
    state_type: StateType
    allow_cancel: bool
    allow_create: bool

    def to_dict(self):
        return {
            "state_type": self.state_type.to_reference_dict(),
            "allow_cancel": self.allow_cancel,
            "allow_create": self.allow_create
        }
