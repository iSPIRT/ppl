import enum
from abc import ABC, abstractmethod
from typing import Tuple

from badal.journal.encoder import JournalEncodeable



class Journalable(JournalEncodeable, ABC):
    @abstractmethod
    def to_journal_stream(self) -> Tuple[str, str]:
        pass
