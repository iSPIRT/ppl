from __future__ import annotations

from typing import Dict, Any

from badal.journal.encoder import JournalEncodeable


class ContractModel(JournalEncodeable):
    def __init__(self, id: str, version: str):
        self.id = id
        self.version = version

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "version": self.version,
        }
    @classmethod
    def from_journal_dict(cls, dict: Dict[str, Any]) -> ContractModel:
        return ContractModel(dict["id"], dict["version"])


class SolidityModel(ContractModel):
    def __init__(self, version: str):
        super(SolidityModel, self).__init__("solidity", version)


solidity_one_oh = SolidityModel("1.0")

