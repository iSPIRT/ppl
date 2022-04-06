import json
from typing import Callable, Any

from badal.schema.model import Specification


class SchemaDecoder(json.JSONDecoder):
    def decode(self, s: str, _w: Callable[..., Any] = ...) -> Any:
        spec = Specification.from_journal_dict(super().decode(s))
        return spec.to_journal_dict()
