from __future__ import annotations

from typing import Tuple, Dict, Any, List

from badal.journal.encoder import JournalType
from badal.journal.main import Journalable
from badal.runtime.proofs.main import ProofRuntime
from badal.schema.attribute_types.base import AttributeType
from badal.schema.attribute_types.detail_types import PublicIdType, AmountType, NotesType
from badal.schema.contracts import ContractModel
from badal.schema.enums import Visibility
from badal.schema.events import EventType
from badal.schema.proofs import ProofModel
from badal.schema.states import StateType
from badal.schema.transactions import TransactionType
from badal.schema.types import SpecAddress


def get_attribute_type(attr_details: dict):
    type = attr_details["type"]
    if type == "public_id":
        return PublicIdType()
    elif type == "amount":
        return AmountType(attr_details["uom"], attr_details["precision"])
    elif type == "notes":
        return NotesType()
    return attr_details


class Schema(Journalable):
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
        self.actions = {}  # Dict[EventType, List[Predicate, Function]]

    def add_attribute_type(self, attribute_type: AttributeType):
        self.attribute_types[attribute_type.id] = attribute_type

    def add_state_type(self, state_type: StateType):
        self.state_types[state_type.id] = state_type

    def add_transaction_type(self, transaction_type: TransactionType):
        self.transaction_types[transaction_type.id] = transaction_type

    # def to_dict(self) -> Dict[str, Any]:
    #     for k, v in self.transaction_types.items():
    #         print(k, v)
    #     data = {
    #         "uri": self.uri,
    #         "name": self.name,
    #         "version": self.version,
    #         "contract_model": {
    #             "id": self.contract_model.id,
    #             "version": self.contract_model.version
    #         },
    #         "proof_model": {
    #             "id": self.proof_model.id,
    #             "version": self.proof_model.version
    #         },
    #         "states": {
    #             k: v.to_dict() for k, v in self.state_types.items()
    #         },
    #         "transactions": {
    #             k: v.to_dict() for k, v in self.transaction_types.items()
    #         },
    #         "depends_upon": [
    #             self.depends_upon
    #         ]
    #     }
    #     return "schema", data

    def to_journal_dict(self, journal_type: JournalType, proof_runtime: ProofRuntime) -> Dict[str, Any]:
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
            "state_types": {
                k: v.to_journal_dict(journal_type, proof_runtime) for k, v in self.state_types.items()
            },
            "transaction_types": [
                v.to_journal_dict(journal_type, proof_runtime) for v in self.transaction_types.values()
            ]
        }

    def to_journal_stream(self, journal_type: JournalType, proof_runtime: ProofRuntime) -> Tuple[str, str]:
        return "global", self.to_journal_dict(journal_type, proof_runtime)

    @classmethod
    def from_journal_dict(cls, dict: Dict[str, Any]) -> Schema:
        spec = Schema(dict["uri"], dict["name"], dict["version"],
                      ContractModel.from_journal_dict(dict["contract_model"]),
                      ProofModel.from_journal_dict(dict["proof_model"]))
        for id, state in dict["state_types"].items():
            attributes = {}
            state_type = StateType(id)
            for attr in state["attributes"]:
                state_type.add_attribute_type(
                    attr["key"]["spec"],
                    attr["key"]["id"],
                    get_attribute_type(attr["value"]),
                    attr["value"]["required"],
                    Visibility(attr["value"]["visibility"])
                )

            spec.add_state_type(state_type)

        for transaction_type in dict["transaction_types"]:
            txn_type = TransactionType.from_journal_dict(transaction_type)
            spec.transaction_types[txn_type.id] = txn_type

        return spec
