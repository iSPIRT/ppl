from abc import ABC

# from badal.schema.states import AttributeDetails


class JournalEncodeableValue(ABC):
    def to_journal_value(self, attr_details: "AttributeDetails") -> str:
        raise NotImplementedError("not implemented")