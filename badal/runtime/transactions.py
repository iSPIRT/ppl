import uuid
from typing import List, Dict, Any

from Crypto.Hash import SHA512
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import pkcs1_15

from badal.errors.result.generic_error import GenericError
from badal.journal.encoder import JournalEncodeable
from badal.runtime.states import State
from badal.schema.transactions import TransactionType


def create_transaction(transaction_type: TransactionType, canceled: List[str], created: List[State]) -> "Transaction":
    transaction_type.states
    allowed_canceled_states = set(
        state_spec.id for state_spec, state in transaction_type.states.items() if state.allow_cancel)
    allowed_created_states = set(
        state_spec.id for state_spec, state in transaction_type.states.items() if state.allow_create)

    disallowed_created_states = [state.state_type.id for state in created if
                                 state.state_type.id not in allowed_created_states]

    if disallowed_created_states:
        raise GenericError("err-disallowed-state-type-in-transaction",
                           {"transaction-type": transaction_type.id, "state-type": disallowed_created_states})

    transaction = Transaction(transaction_type, canceled, created)
    return transaction


class Transaction(JournalEncodeable):
    def __init__(self, transaction_type: TransactionType, canceled: List[str], created: List[State]):
        self.transaction_type = transaction_type
        self.id: str = str(uuid.uuid4())
        self.canceled = canceled
        self.created = created
        self.signatures: Dict[str, str] = {}

    def __str__(self):
        return f"Transaction({self.transaction_type.id}:{self.id}\n  Canceled->{self.canceled}\n  Created->{self.created})"

    def sign(self, key: RsaKey):
        # todo .. dict to str conversion needs to be constant
        to_be_signed = str(self.to_journal_dict()["body"])
        hash = SHA512.new(bytes(to_be_signed, "utf-8"))
        signature = pkcs1_15.new(key).sign(hash).hex()
        # todo .. get the correct form for public key
        self.signatures[str(key.publickey)] = signature
        print(self.to_journal_dict())

    def to_journal_dict(self) -> Dict[str, Any]:
        return {
            "body": {
                "id": self.id,
                "type": self.transaction_type.id
            },
            "envelope": {
                "signatures": {k: v for k, v in self.signatures.items()}
            }
        }
