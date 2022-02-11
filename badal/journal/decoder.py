import json
from typing import Callable, Any

from badal.schema.attribute_types import PublicIdType, AmountType, NotesType
from badal.schema.contracts import ContractModel
from badal.schema.model import Specification
from badal.schema.proofs import ProofModel
from badal.schema.states import StateType
from badal.schema.types import GlobalId


def get_attribute_type(attr_details: dict):
    type = attr_details["type"]["type"]
    if type == "public_id":
        return PublicIdType()
    elif type == "amount":
        return AmountType(attr_details["type"]["uom"], attr_details["type"]["precision"])
    elif type == "notes":
        return NotesType()
    return attr_details


class SchemaDecoder(json.JSONDecoder):
    def decode(self, s: str, _w: Callable[..., Any] = ...) -> Any:
        tmp = super().decode(s)
        contract_model = tmp["contract_model"]
        proof_model = tmp["proof_model"]
        spec = Specification(tmp["uri"], tmp["name"], tmp["version"],
                             ContractModel(contract_model["id"], contract_model["version"]),
                             ProofModel(proof_model["id"], proof_model["version"]))
        for id, state in tmp["states"].items():
            attributes = {}
            for attr in state["attributes"]:
                attributes[GlobalId(attr["key"]["id"], attr["key"]["spec"])] = get_attribute_type(attr["value"])
            spec.add_state_type(StateType(id))
            spec.attribute_types = attributes
        return spec.to_dict()
