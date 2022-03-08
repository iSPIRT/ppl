from __future__ import annotations

from typing import Dict, Any

from badal.journal.encoder import JournalEncodeable


class ProofModel(JournalEncodeable):
    def __init__(self, id: str, version: str):
        self.id = id
        self.version = version

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "version": self.version,
        }

    @classmethod
    def from_journal_dict(cls, dict: Dict[str, Any]) -> ProofModel:
        return ProofModel(dict["id"], dict["version"])


class ZokratesModel(ProofModel):
    def __init__(self, version: str):
        super(ZokratesModel, self).__init__("zokrates", version)


zokrates_one_oh = ZokratesModel("1.0")
