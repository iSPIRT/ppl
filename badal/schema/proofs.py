from __future__ import annotations

import abc
import hashlib
from abc import abstractmethod
from typing import Dict, Any, Tuple

from badal.journal.encoder import JournalEncodeable, JournalType
from badal.runtime.proofs.main import ProofRuntime
from badal.runtime.proofs.zokrates import ZokratesRuntime


class ProofModel(JournalEncodeable):
    registry: Dict[Tuple[str,str], ProofModel] = {}
    def __init__(self, id: str, version: str):
        self.id = id
        self.version = version
        if (self.id, self.version) not in ProofModel.registry:
            ProofModel.registry[(self.id, self.version)] = self

    def to_journal_dict(self, journal_type: JournalType, proof_runtime: ProofRuntime) -> Dict[str, Any]:
        return {
            "id": self.id,
            "version": self.version,
        }

    @classmethod
    def from_journal_dict(cls, dict: Dict[str, Any]) -> ProofModel:
        return ProofModel.registry[(dict["id"], dict["version"])]

    @classmethod
    @abstractmethod
    def get_proof_runtime(cls) -> ProofRuntime:
        pass


class ZokratesModel(ProofModel):
    def __init__(self, version: str):
        super(ZokratesModel, self).__init__("zokrates", version)

    @classmethod
    def get_proof_runtime(cls) -> ProofRuntime:
        return ZokratesRuntime()


zokrates_one_oh = ZokratesModel("1.0")
