import hashlib
from typing import Any

from badal.runtime.proofs.main import ProofRuntime


class ZokratesRuntime(ProofRuntime):
    @classmethod
    def hash(self, value: Any) -> str:
        m = hashlib.sha1()
        m.update(value)
        return m.digest().hex()

