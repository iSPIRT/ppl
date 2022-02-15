from dataclasses import dataclass
from typing import Dict, Tuple

from badal.schema.states import StateDetails, StateType
from badal.schema.types import SpecAddress


class TransactionType:
    def __init__(self, id: str):
        self.id = id
        self.states: Dict[Tuple[SpecAddress, str], StateDetails] = {}

    def __str__(self):
        return f"TransactionType({self.id})"

    def add_state_type(self, state_type: StateType, allow_cancel: bool = True, allow_create: bool = True):
        self.states[state_type.id] = StateDetails(state_type, allow_cancel, allow_create)

    def to_dict(self):
        return {
            "id": self.id,
            "states": {
                k: v.to_dict() for k, v in self.states.items()
            }
        }

    def to_reference_dict(self):
        return {
            "id": self.id,
            "states": {
                k: v.to_reference_dict() for k, v in self.states.items()
            }
        }


@dataclass
class TransactionDetails:
    state_type: TransactionType
    allow_cancel: bool
    allow_create: bool
