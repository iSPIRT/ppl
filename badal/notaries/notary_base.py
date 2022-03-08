import json
from typing import Dict

from typing.io import TextIO

from badal.journal.encoder import JournalEncoder
from badal.journal.main import Journalable
from badal.runtime.transactions import Transaction


class Notary:
    def __init__(self):
        self.journals: Dict[str, TextIO] = {}

    def add_journal(self, id, fp: TextIO):
        self.journals[id] = fp

    def read_spec(self):
        pass

    def notarise(self, value: Journalable) -> str:
        stream, _ = value.to_journal_stream()
        json_str = json.dumps(value, sort_keys=True, indent=2, cls=JournalEncoder)
        if stream in self.journals:
            json.dump(value, self.journals[stream], sort_keys=True, indent=2, cls=JournalEncoder)
        return json_str

    def notarise_transaction(self, transaction: Transaction):
        print(f"Notarising transaction {transaction}")
