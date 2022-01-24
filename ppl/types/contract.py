from decimal import Decimal

from ppl.types.iou import ContractType
from ppl.types.state import StateType, SerialisedState, State
from ppl.types.value_store import ValueStore, UOM
from ppl.types.wallet import Wallet


class Contract(ValueStore):
    state_type = StateType.Contract

    def __init__(self, state_id: int, contract_type: ContractType, own_wallet: Wallet, uom: UOM, amount: Decimal):
        super().__init__(state_id, uom, amount)
        self.contract_type = contract_type
        self.own_wallet = own_wallet

    def __str__(self):
        return "Contract {}->{}:{} {}".format(self.contract_type, self.own_wallet, self.uom, self.amount)

    def __eq__(self, other):
        return isinstance(other, Contract) \
               and self.contract_type.value == other.contract_type.value \
               and self.own_wallet.id == other.own_wallet.id \
               and self.uom == other.uom \
               and self.amount == other.amount


def serialise(self) -> SerialisedState:
    """Convert state data into a generic serialised state for further handling in an abstract way by the platform"""
    return SerialisedState(
        self.state_type.value,
        self.state_id,
        {
            "uom": self.uom.value,
            "amount": self.amount,
            "contract_type": self.contract_type.value,
            "own_wallet_id": self.own_wallet.id,
        }, {

        }
    )


@staticmethod
def deserialise(ecosystem: 'Ecosystem', dct: SerialisedState):
    """Reconstruct an IOU from a serialised state"""
    instance = Contract(dct["state_id"],
                   Contract(dct["public"]["contract_type"]),
                   ecosystem.get_wallet_for_id(dct["public"]["own_wallet_id"]),
                   UOM(dct["public"]["uom"]),
                   Decimal(dct["public"]["amount"]))
    instance.state_id = dct["state_id"]
    return instance


State.deserialisers[StateType.IOU.value] = deserialise
