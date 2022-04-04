import uuid
from typing import Dict, Any

from badal.errors.result.validation_error import ValidationError
from badal.journal.encoder import JournalEncodeable
from badal.schema.states import StateType
from badal.schema.types import GlobalId


def create_state(state_type: StateType, attrs: Dict[str, Any]):
    validation_results = [[(k.id, err) for err in attr_details.validate(attrs[k.id])] for k, attr_details in
                          state_type.attributes.items()]
    flattened_validation_results = [item for sublist in validation_results for item in sublist]
    if flattened_validation_results:
        raise ValidationError(flattened_validation_results)
    else:
        return State(state_type, attrs)


class State(JournalEncodeable):
    def __init__(self, state_type: StateType, attrs: Dict[str, Any]):
        self.state_type = state_type
        self.id: str = str(uuid.uuid4())
        self.attrs = attrs

    def __str__(self):
        return f"State({self.state_type.id}:{self.id}:{self.attrs})"

    def __repr__(self):
        return f"State({self.state_type.id}:{self.id})"

    def to_journal_dict(self) -> Dict[str, Any]:
        foo = 3
        return {
            "id": self.id,
            "type": self.state_type.id,
            "attrs": {k: v.to_journal_value(self.state_type.attributes[GlobalId("_", k)]) for k, v in
                      self.attrs.items()}
        }
