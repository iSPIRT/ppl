import itertools
from enum import Enum
from typing import Callable, Mapping, Any


class StateType(Enum):
    """Different states can be stored on the ledger. StateType disambiguates which state is being stored"""
    State = "STT"
    IOU = "IOU"
    Contract = "CON"


class SerialisedState:
    """A serialised state is a generic structure for unbundling any state into dictionaries and separating these
    into public and private data"""
    def __init__(self, state_type: int, state_id: int, private: dict, public: dict):
        self.state_type = state_type
        self.state_id = state_id
        self.private = private
        self.public = public

    def to_json(self):
        """This returns a dict which is the standardised structure for serialising all states into json"""
        return {
            "state_type": self.state_type,
            "state_id": self.state_id,
            "public": self.public,
            "private": self.private
        }


class State:
    """A state is anything that can be stored on the ledger and changes representation over time"""
    next_id = itertools.count().__next__

    def __init__(self, state_id):
        self.state_id = state_id

    def serialise(self) -> SerialisedState:
        """This is to be implemented by subclasses to do necessary serialisations"""
        raise NotImplementedError

    subclasses: Mapping[int, Any] = {}
    deserialisers: Mapping[int, Callable[[], 'State']] = {}


def deserialise_state(ecosystem: 'Ecosystem', dct):
    state_type = int(dct["state_type"])
    clsmethod = State.deserialisers[state_type].__get__(State.subclasses[state_type])
    return clsmethod(ecosystem, dct)
