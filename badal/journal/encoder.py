import enum
import json
from abc import ABC
from typing import Dict, Any

class JournalEncodeable(ABC):
    def to_journal_dict(self) -> Dict[str, Any]:
        raise NotImplementedError("not implemented")


class JournalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, JournalEncodeable):
            return obj.to_journal_dict()
        elif isinstance(obj, enum.Enum):
            return obj.value
        return json.JSONEncoder.default(self, obj)


