import itertools


class Wallet:
    next = itertools.count().__next__()

    def __init__(self, code, key, journal):
        self.code = code
        self.key = key
        self.journal = journal
        journal.register_wallet(self)

    def __str__(self):
        return "W({}:{})".format(self.id, self.code)
