import unittest
import uuid
from datetime import datetime

from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ppl.database.model import Base, Entity, Schema, SchemaState, State, StateValidity, IOU, Transaction, Wallet
from tests.utils.url import url

engine = create_engine(url, echo=True, future=True)
Session = sessionmaker(bind=engine)


class TestLedgerOperations(unittest.TestCase):
    def test_basic_ledger_operations(self):
        Base.metadata.bind = engine
        with engine.connect() as conn:
            Base.metadata.drop_all()
            Base.metadata.create_all()

            keypair = rsa.generate_private_key(
                backend=crypto_default_backend(),
                public_exponent=65537,
                key_size=2048
            )
            private_key = keypair.private_bytes(
                crypto_serialization.Encoding.PEM,
                crypto_serialization.PrivateFormat.PKCS8,
                crypto_serialization.NoEncryption())
            public_key = keypair.public_key().public_bytes(
                crypto_serialization.Encoding.OpenSSH,
                crypto_serialization.PublicFormat.OpenSSH
            )
            rbi = Entity(uuid.uuid4(), "Reserve Bank of India")
            cbdc_schema = Schema(uuid.uuid4(), "RBI CBDC", 1)
            iou_schema_state = SchemaState(uuid.uuid4(), "IOU", cbdc_schema)
            cbdc_wallet = Wallet(uuid.uuid4(), "rbi_cbdc", public_key)
            transaction = Transaction(uuid.uuid4())
            some_state = State(uuid.uuid4(), uuid.uuid4(), 1, datetime.now(), StateValidity.Active, None,
                               {"foo": "bar1"},
                               {"buz": "fiz1"})

            session = Session()

            session.add_all((rbi, cbdc_schema, cbdc_wallet, transaction, some_state))
            transaction.create_state(some_state)
            session.commit()
            new_transaction = Transaction(uuid.uuid4())
            mutated_state = some_state.mutate(uuid.uuid4(), new_transaction, datetime.now(),
                                              lambda p, q: ({"foo": "bar2"}, {"buz": "fiz2"}))
            session.add_all((new_transaction, mutated_state,))
            session.commit()

            iou_transaction = Transaction(uuid.uuid4())
            iou = IOU(uuid.uuid4(), uuid.uuid4(), 1, datetime.now(), StateValidity.Active, None, {"iou1": "value1"},
                      {"iou2": "value2"})
            iou_transaction.create_state(iou)
            session.add_all((iou_transaction, iou,))
            session.commit()
