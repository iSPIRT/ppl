from dataclasses import dataclass
from typing import TypeAlias, Dict, Any

from badal.journal.encoder import JournalEncodeable

SpecAddress: TypeAlias = str


@dataclass(frozen=True, eq=True)
class GlobalId(JournalEncodeable):
    spec: SpecAddress
    id: str

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "spec": self.spec,
            "id": self.id
        }
