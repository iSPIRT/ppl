from typing import List

import uuid
from badal.runtime.states import State
from badal.schema.transactions import TransactionType


class Transaction():
    def __init__(self, transaction_type: TransactionType, canceled: List[str], created: List[State]):
        self.transaction_type = transaction_type
        self.id: str = str(uuid.uuid4())
        self.canceled = canceled
        self.created = created

    def __str__(self):
        return f"Transaction({self.transaction_type.id}:{self.id}\n  Canceled->{self.canceled}\n  Created->{self.created})"