from abc import ABC

from badal.journal.encoder import JournalType
from badal.schema.proofs import ProofModel


class JournalEncodeableValue(ABC):
    def to_journal_value(self, attr_details: "AttributeDetails", journal_type: JournalType, proof_model: ProofModel) -> str:
        raise NotImplementedError("not implemented")