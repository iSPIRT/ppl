import itertools
import logging
from enum import Enum

journals = {}
journals_for_wallet = {}

log = logging.getLogger("Journal")


class JournalActivity(Enum):
    CreateState = 1


class Journal:
    next_id = itertools.count().__next__

    def __init__(self, code):
        self.id = self.next_id()
        self.code = code
        self.next_wallet_id = itertools.count().__next__
        self.own_wallets = {}
        self.active_states = {}
        self.audit_log = []
        journals[self.id] = self

    def __str__(self):
        return "J({}:{})".format(self.id, self.code)

    def register_wallet(self, wallet):
        wallet.id = self.next_wallet_id()
        self.own_wallets[wallet.id] = wallet
        journals_for_wallet[wallet.id] = self

    def record_state(self, state):
        self.active_states[state.id] = state
        log.debug("Journal {} recorded state {}".format(self, state))
        self.audit_log.append((JournalActivity.CreateState, state))

    def show_global_state(self):
        print("Journal Global State for {}:{}".format(self.id, self.code))
        print("  Active states are")
        for state in self.active_states.values():
            print("    {}".format(state))
