import itertools
import logging

from dinero.types.iou import StateType
from dinero.types.journal import journals

notaries = {}
notaries_by_code = {}

log = logging.getLogger("Notary")


class Notary:
    next = itertools.count().__next__

    def __init__(self, code):
        self.id = Notary.next()
        self.code = code
        self.states = {}
        notaries[self.id] = self
        notaries_by_code[code] = self
        log.debug("Created notary: {}".format(self))

    def __str__(self):
        return "N({}:{})".format(self.id, self.code)

    def create_iou(self, iou):
        self.states[iou.id] = iou.to_public_record()
        log.debug("Creating IOU {}".format(iou))

        journals = set(wallet.journal for wallet in (iou.from_wallet, iou.to_wallet))
        for journal in journals:
            journal.record_state(iou)

    create_states = {StateType.IOU:  create_iou}

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