from dataclasses import dataclass
from typing import Dict

from badal.journal.encoder import JournalType
from badal.runtime.proofs.main import ProofRuntime
from badal.schema.states import StateDetails, StateType
from badal.schema.types import GlobalId


class TransactionType:
    def __init__(self, id: str):
        self.id = id
        self.states: Dict[GlobalId, StateDetails] = {}

    def __str__(self):
        return f"TransactionType({self.id})"

    def add_state_type(self, spec: str, state_type: StateType, allow_cancel: bool = True, allow_create: bool = True):
        state_type_id = GlobalId(spec=spec, id=state_type.id)
        sd = StateDetails(spec, state_type.id, allow_cancel, allow_create)
        self.states[state_type_id] = sd

    def to_journal_dict(self, journal_type: JournalType, proof_runtime: ProofRuntime):
        return {
            "id": self.id,
            "states": [v.to_journal_dict(journal_type, proof_runtime) for v in self.states.values()]
        }

    @classmethod
    def from_journal_dict(cls, dict: Dict) -> "TransactionType":
        txn_type = TransactionType(dict["id"])
        state_details = {}
        for state_data in dict["states"]:
            st = StateDetails.from_journal_dict(state_data)
            state_details[GlobalId(st.spec, st.state_type)] = st
        txn_type.states = state_details
        return txn_type
        # for state_details in txn_type["states"]:
        #     StateDetails()


@dataclass
class TransactionDetails:
    state_type: TransactionType
    allow_cancel: bool
    allow_create: bool
