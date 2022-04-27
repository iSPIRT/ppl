import enum
import json
from abc import ABC
from typing import Dict, Any

from badal.runtime.proofs.main import ProofRuntime
from badal.runtime.proofs.zokrates import ZokratesRuntime


class JournalType(enum.Enum):
    Private = "prv"
    Public = "pub"


class JournalEncodeable(ABC):
    def to_journal_dict(self, journal_type: JournalType, proof_runtime: ProofRuntime) -> Dict[str, Any]:
        raise NotImplementedError("not implemented")


class JournalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, JournalEncodeable):
            return obj.to_journal_dict(JournalType.Private, ZokratesRuntime())
        elif isinstance(obj, enum.Enum):
            return obj.value
        return json.JSONEncoder.default(self, obj)
