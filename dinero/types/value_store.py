from enum import Enum

from dinero.types.state import State


class UOM(Enum):
    Currency_INR = 1
    Others = 99


class ValueStore(State):
    def __init__(self, state_id, uom, amount):
        super().__init__(state_id)
        self.uom = uom
        self.amount = amount
