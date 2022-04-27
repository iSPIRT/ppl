import json
from typing import Dict

from typing.io import TextIO

from badal.journal.encoder import JournalEncoder, JournalType
from badal.journal.main import Journalable
from badal.runtime.proofs.main import ProofRuntime
from badal.runtime.transactions import Transaction


class Notary:
    def __init__(self):
        self.journals: Dict[str, TextIO] = {}

    def add_journal(self, id, fp: TextIO):
        self.journals[id] = fp

    def read_spec(self):
        pass

    def notarise(self, value: Journalable, journal_type: JournalType, proof_runtime: ProofRuntime) -> str:
        stream, _ = value.to_journal_stream(journal_type, proof_runtime)
        json_str = json.dumps(value, sort_keys=True, indent=2, cls=JournalEncoder)
        if stream in self.journals:
            json.dump(value, self.journals[stream], sort_keys=True, indent=2, cls=JournalEncoder)
        return json_str

    def notarise_transaction(self, transaction: Transaction, journal_type: JournalType, proof_runtime: ProofRuntime):
        txn_json = json.dumps(transaction.to_journal_dict(journal_type, proof_runtime), indent=2)
        print(f"Notarising transaction {txn_json}")
