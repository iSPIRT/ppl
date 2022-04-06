from abc import ABC

class JournalEncodeableValue(ABC):
    def to_journal_value(self, attr_details: "AttributeDetails") -> str:
        raise NotImplementedError("not implemented")