import abc
from typing import Any


class ProofRuntime(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def hash(self, value: Any) -> str:
        pass
