import logging

log = logging.getLogger("Transaction")


class Transaction:
    def __init__(self, dropped_state_ids, created_states, remarks):
        self.dropped_state_ids = dropped_state_ids
        self.created_states = created_states
        self.remarks = remarks
        log.debug("Created transaction for: {}".format(self.remarks))

