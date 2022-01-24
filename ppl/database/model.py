from __future__ import annotations

import enum
import itertools
import uuid
from datetime import datetime
from typing import Optional, Callable, Tuple

from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME, Enum
from sqlalchemy.orm import declarative_base, relationship

from ppl.database.typedecorators.guid import GUID
from ppl.database.typedecorators.json import JsonData
from ppl.types.state import StateType

Base = declarative_base()


class Entity(Base):
    __tablename__ = 'entities'
    id = Column(GUID, primary_key=True)
    name = Column(String(64))

    def __init__(self, id, name):
        self.id = id
        self.name = name


class Schema(Base):
    __tablename__ = "ppl_schemas"
    id = Column(GUID, primary_key=True)
    name = Column(String(64), nullable=False)
    version = Column(Integer, nullable=False)
    entity_id = Column(GUID, ForeignKey('entities.id'))

    def __init__(self, id, name, version):
        self.id = id
        self.name = name
        self.version = version


class SchemaState(Base):
    __tablename__ = "schema_states"
    id = Column(GUID, primary_key=True)
    name = Column(String(64))
    schema_id = Column(GUID, ForeignKey("ppl_schemas.id"))

    def __init__(self, id, name, schema_id):
        self.id = id
        self.name = name
        self.schema_id = schema_id


class Wallet(Base):
    __tablename__ = 'wallets'
    next_id = itertools.count().__next__

    id = Column(GUID, primary_key=True)
    handle = Column(String(16))
    public_key = Column(String(512))

    def __init__(self, id, handle, public_key):
        self.id = id if id else Wallet.next_id()
        self.handle = handle
        self.public_key = public_key


class StateValidity(enum.Enum):
    Proposed = "P"
    Active = "A"
    Extinguished = "E"


class State(Base):
    __tablename__ = 'states'

    next_id = itertools.count().__next__

    id = Column(GUID, primary_key=True)
    logical_id = Column(GUID)
    version = Column(Integer)
    prior_id = Column(GUID, nullable=True)
    creator_id = Column(GUID, ForeignKey("transactions.id"), nullable=False)
    destroyer_id = Column(GUID, ForeignKey("transactions.id"), nullable=True)
    created = Column(DATETIME)
    state_type = Column(Enum(StateType))
    validity = Column(Enum(StateValidity))
    public = Column(JsonData(4000))
    proof = Column(JsonData(4000))

    creator = relationship("Transaction", foreign_keys=[creator_id])
    destroyer = relationship("Transaction", foreign_keys=[destroyer_id])

    __mapper_args__ = {
        'polymorphic_on': state_type,
        'polymorphic_identity': StateType.State
    }

    def __init__(self, id: uuid.UUID, logical_id: uuid.UUID, version: int, created: datetime,
                 validity: StateValidity, prior_id: Optional[uuid.UUID],
                 public: dict, proofs: dict):
        self.id = id
        self.logical_id = logical_id
        self.version = version
        self.created = created
        self.prior_id = prior_id
        self.validity = validity
        self.public = public
        self.proofs = proofs

    def mutate(self, id: uuid.UUID, new_transaction: Transaction, created: datetime, mutator: Callable[[dict, dict], Tuple[dict, dict]]) -> State:
        new_public, new_proofs = mutator(self.public, self.proofs)
        self.validity = StateValidity.Extinguished
        new_state = State(id, self.logical_id, self.version + 1, created, StateValidity.Active, self.id, new_public,
                          new_proofs)
        new_transaction.destroy_state(self)
        new_transaction.create_state(new_state)
        return new_state


class IOU(State):
    __tablename__ = 'states'

    __mapper_args__ = {
        'polymorphic_identity': StateType.IOU
    }

    def __init__(self, id: uuid.UUID, logical_id: uuid.UUID, version: int, created: datetime,
                 validity: StateValidity, prior_id: Optional[uuid.UUID],
                 public: dict, proofs: dict):
        super().__init__(id, logical_id, version, created, validity, prior_id, public, proofs)


class Contract(State):
    __tablename__ = 'states'

    __mapper_args__ = {
        'polymorphic_identity': StateType.Contract
    }


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(GUID, primary_key=True)


    def __init__(self, id: uuid.UUID):
        self.id = id

    def create_state(self, state: State):
        if state.creator_id is None:
            state.creator_id = self.id
        else:
            raise Exception("State already initialised by another transaction")

    def destroy_state(self, state: State):
        if state.creator_id is None:
            raise Exception("State not yet created")
        elif state.destroyer_id is not None:
            raise Exception("State has already been destroyed by another transaction")
        else:
            state.destroyer_id = self.id
