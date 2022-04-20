from dataclasses import dataclass
from typing import Dict, Any, List

from badal.errors.Invalidity import Invalidity
from badal.journal.encoder import JournalEncodeable, JournalType
from badal.runtime.proofs.main import ProofRuntime
from badal.schema.attribute_types.attribute_type_registry import registry
from badal.schema.attribute_types.base import AttributeType
from badal.schema.enums import Visibility
from badal.schema.types import GlobalId


@dataclass
class AttributeDetails(JournalEncodeable):
    id: str
    attr_type_id: str
    required: bool
    visibility: Visibility

    def validate(self, value: Any) -> List[Invalidity]:
        print(f"Fetching {self.attr_type_id}")
        return registry[self.attr_type_id].validate(value)

    def to_journal_dict(self, journal_type: JournalType, proof_runtime: ProofRuntime) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.attr_type_id,
            "required": self.required,
            "visibility": self.visibility
        }


class StateType(JournalEncodeable):
    def __init__(self, id: str):
        self.id = id
        # self.attributes: Dict[GlobalId, Dict[str, Any]] = {}
        self.attributes: Dict[GlobalId, AttributeType] = {}

    def add_attribute_type(self, spec: str, id: str, type: AttributeType, required: bool = True,
                           visibility: Visibility = Visibility.Private):
        registry[type.id] = type
        self.attributes[GlobalId(spec=spec, id=id)] = type

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

    def to_journal_dict(self, journal_type: JournalType, proof_runtime: ProofRuntime) -> Dict[str, Any]:
        return {
            "id": self.id,
            "attributes": [{"key": k, "value": v.to_journal_dict(journal_type, proof_runtime)} for k, v in self.attributes.items()]
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

    def to_journal_dict(self, journal_type: JournalType, proof_runtime: ProofRuntime) -> Dict[str, Any]:
        return {
            "spec": self.spec,
            "state_type": self.state_type,
            "allow_cancel": self.allow_cancel,
            "allow_create": self.allow_create
        }

    @classmethod
    def from_journal_dict(cls, dict: Dict[str, Any]) -> "StateDetails":
        return StateDetails(dict["spec"], dict["state_type"], dict["allow_cancel"], dict["allow_create"])
