from __future__ import annotations

from typing import TYPE_CHECKING

from dinero.types.transaction import Transaction

if TYPE_CHECKING:
    from dinero.types.ecosystem import Ecosystem

import itertools
import logging

from dinero.types.iou import StateType
from dinero.types.notary_journal import NotaryJournal

log = logging.getLogger("Notary")


class Notary:
    next = itertools.count().__next__

    def __init__(self, code, ecosystem: Ecosystem):
        self.id = Notary.next()
        self.code = code
        self.states = {}
        self.journal = NotaryJournal()
        self.ecosystem = ecosystem
        self.ecosystem.add_notary(self)
        log.debug("Created notary: {}".format(self))

    def __str__(self):
        return "N({}:{})".format(self.id, self.code)

    def record(self, transaction=Transaction):
        wallet_providers = {state.from_wallet.id for state in transaction.created_states} \
            .update({state.to_wallet.id for state in transaction.created_states})
        log.debug("Wallet providers are {}".format(wallet_providers))

    def create_iou(self, iou):
        self.states[iou.id] = iou.to_public_record()
        log.debug("Creating IOU {}".format(iou))

        journals = set(wallet.journal for wallet in (iou.from_wallet, iou.to_wallet))
        for journal in journals:
            journal.record_state(iou)

    create_states = {StateType.IOU: create_iou}

    def create_state(self, state):
        Notary.create_states[state.state_type](self, state)

    def show_global_state(self):
        print("Notary Global State for {}:{}".format(self.id, self.code))
        print("  Active states are")
        for state in self.active_states.values():
            print("    {}".format(state))


def show_global_state():
    for notary in notaries.values():
        notary.show_global_state()
    for journal in journals.values():
        journal.show_global_state()
