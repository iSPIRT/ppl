from typing import List

from badal.errors.Invalidity import Invalidity


class ValidationError(Exception):
    def __init__(self, invalidities: List[Invalidity]):
        self.invalidities = invalidities