from typing import Tuple, Dict, Any, List

from badal.schema.attribute_types import AttributeType
from badal.schema.contracts import ContractModel
from badal.schema.events import EventType
from badal.schema.proofs import ProofModel
from badal.schema.states import StateType
from badal.schema.transactions import TransactionType
from badal.schema.types import SpecAddress
from badal.journal.main import Journalable


class Specification(Journalable):
    def __init__(self, uri: str, name: str, version: str, contract_model: ContractModel,
                 proof_model: ProofModel):
        self.uri = uri
        self.name = name
        self.version = version
        self.contract_model = contract_model
        self.proof_model = proof_model
        self.attribute_types: Dict[str, AttributeType] = {}
        self.event_types: Dict[str, EventType] = {}
        self.state_types: Dict[str, StateType] = {}
        self.transaction_types: Dict[str, TransactionType] = {}
        self.depends_upon: List[SpecAddress] = []
        self.actions  = {} # Dict[EventType, List[Predicate, Function]]

    def add_attribute_type(self, attribute_type: AttributeType):
        self.attribute_types[attribute_type.id] = attribute_type

    def add_state_type(self, state_type: StateType):
        self.state_types[state_type.id] = state_type

    def add_transaction_type(self, transaction_type: TransactionType):
        self.transaction_types[transaction_type.id] = transaction_type

    def to_dict(self) -> Dict[str, Any]:
        for k, v in self.transaction_types.items():
            print(k, v)
        data = {
            "uri": self.uri,
            "name": self.name,
            "version": self.version,
            "contract_model": {
                "id": self.contract_model.id,
                "version": self.contract_model.version
            },
            "proof_model": {
                "id": self.proof_model.id,
                "version": self.proof_model.version
            },
            "states": {
                k: v.to_dict() for k, v in self.state_types.items()
            },
            "transactions": {
                k: v.to_dict() for k, v in self.transaction_types.items()
            },
            "depends_upon": [
                self.depends_upon
            ]
        }
        return "schema", data

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "uri": self.uri,
            "name": self.name,
            "version": self.version,
            "contract_model": {
                "id": self.contract_model.id,
                "version": self.contract_model.version
            },
            "proof_model": {
                "id": self.proof_model.id,
                "version": self.proof_model.version
            },
            "states": self.state_types,
            # {
            #     k: v.to_dict() for k, v in self.state_types.items()
            # },
        }

    def to_journal_stream(self) -> Tuple[str, str]:
        return "global", self.to_journal_dict()
