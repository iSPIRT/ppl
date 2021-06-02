import logging
from decimal import Decimal
from enum import Enum

from dinero.types.journal import journals_for_wallet, get_wallet_for_id
from dinero.types.state import State, SerialisedState, StateType
from dinero.types.wallet import Wallet

log = logging.getLogger("IOU")


class IOUType(Enum):
    """A subclass of State is an IOU. IOU themselves are of multiple types. This enum disambiguates the type of IOU"""
    Currency = 1
    AccountDeposit = 2
    Loan = 3


class IOU(State):
    """An IOU is a subclass of State which expresses a liability from a `from_wallet` to a `to_wallet` for a given
    amount """
    state_type = StateType.IOU

    def __init__(self, state_id: int, iou_type: IOUType, from_wallet: Wallet, to_wallet: Wallet, amount: Decimal):
        super().__init__(state_id)
        self.iou_type = iou_type
        self.from_wallet = from_wallet
        self.to_wallet = to_wallet
        self.amount = amount

    def __str__(self):
        return "IOU {}->{}:{}".format(self.from_wallet, self.to_wallet, self.amount)

    def __eq__(self, other):
        return isinstance(other, IOU) \
                and self.iou_type.value == other.iou_type.value \
                and self.from_wallet.id == other.from_wallet.id \
                and self.to_wallet.id == other.to_wallet.id \
                and self.amount == other.amount

    def serialise(self) -> SerialisedState:
        """Convert state data into a generic serialised state for further handling in an abstract way by the platform"""
        return SerialisedState(
            self.state_type.value,
            self.state_id,
            {
                "amount": self.amount
            }, {
                "iou_type": self.iou_type.value,
                "from_wallet_id": self.from_wallet.id,
                "to_wallet_id": self.to_wallet.id,
            }
        )

    @staticmethod
    def deserialise(dct: SerialisedState):
        """Reconstruct an IOU from a serialised state"""
        instance = IOU(dct["state_id"],
                       IOUType(dct["public"]["iou_type"]),
                       get_wallet_for_id(dct["public"]["from_wallet_id"]),
                       get_wallet_for_id(dct["public"]["to_wallet_id"]),
                       Decimal(dct["private"]["amount"]))
        instance.state_id = dct["state_id"]
        return instance

    State.deserialisers[StateType.IOU.value] = deserialise


# register subclass with state register
State.subclasses[StateType.IOU.value] = IOU
