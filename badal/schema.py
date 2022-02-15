from __future__ import annotations

import json
from abc import ABC, abstractmethod

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey

from badal.journal.decoder import SchemaDecoder
from badal.notaries.notary_base import Notary
from badal.schema.attribute_types import PublicIdType, AmountType, NotesType, Visibility
from badal.schema.contracts import solidity_one_oh
from badal.schema.model import Specification
from badal.schema.proofs import zokrates_one_oh
from badal.schema.states import StateType
from badal.schema.transactions import TransactionType


class PplId:
    pass


class PplId(ABC):
    @abstractmethod
    def public_key_str(self) -> str:
        pass


class RsaPplId(PplId):
    def __init__(self, keypair: RsaKey):
        self.keypair = keypair


class AttributeDescriptor:
    def __init__(self, id: str, name: str, type: str):
        self.id = id
        self.name = name
        self.type = type


def generate_keypair() -> RsaKey:
    return RSA.generate(2048)


if __name__ == "__main__":
    # rbi_id = RsaPplId(generate_keypair())
    # bank_id = RsaPplId(generate_keypair())
    # person1_id = RsaPplId(generate_keypair())

    spec_core = Specification("http://ispirt.org/pplspecs/core", "PPL Core Schema", "0.1", solidity_one_oh,
                              zokrates_one_oh)
    ## we need a capability to add meta attribute types here .. eg.
    ## This feature is available only for the global root specification since it requires addition of IdType classes
    ## with behaviours. Other specs cannot add this. However the id can then be used instead of instantiating the class
    ## directly when add_attribute_type is used on other states
    # spec_core.add_meta_attribute_type("public_id", PublicIdType)

    notary = Notary()
    journal1 = open("journals/global", "w")
    notary.add_journal("global", journal1)
    journal2 = open("journals/cbdc", "w")
    notary.add_journal("cbdc", journal2)

    notary.notarise(spec_core)

    spec_cbdc = Specification("http://ispirt.org/rbi_cbdc/spec", "RBI CBDC Schema", "0.1", solidity_one_oh,
                              zokrates_one_oh)

    cbdc_state_type = StateType("cbdc")
    cbdc_state_type.add_attribute_type("_", "from", PublicIdType())
    cbdc_state_type.add_attribute_type("_", "to", PublicIdType())
    cbdc_state_type.add_attribute_type("_", "amount", AmountType("cbdc_inr", precision=3))
    cbdc_state_type.add_attribute_type("_", "notes", NotesType(maxlen=128), visibility=Visibility.Public)

    spec_cbdc.add_state_type(cbdc_state_type)

    cbdc_transfer_type = TransactionType("transfer")
    cbdc_transfer_type.add_state_type(cbdc_state_type)

    spec_cbdc.add_transaction_type(cbdc_transfer_type)
    cbdc_json_str = notary.notarise(spec_cbdc)
    print(cbdc_json_str)
    cbdc_decoded = json.loads(cbdc_json_str, cls=SchemaDecoder)
    print(cbdc_decoded)

    # notary = Notary()
    # notary.update_specification(spec_core)
    # notary.update_specification(spec_cbdc)
    # notary.notarise_transaction(
    #     Transaction(type="http://ispirt.org/rbi_cbdc/transactions/transfer",
    #                 new_states=[State("http://ispirt.org/rbi_cbdc/states/cbdc",
    #                                   {
    #                                       "from": bank_id.to_public_key(),
    #                                       "to": person1_id.to_public_key()
    #                                   }
    #                                   )]))
    #
    # issuer = PublicIdType()
    # owner = PublicIdType()
