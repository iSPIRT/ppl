import json
from typing import Callable, Any

from badal.journal.encoder import JournalType
from badal.schema.model import Schema


class SchemaDecoder(json.JSONDecoder):
    def decode(self, s: str, _w: Callable[..., Any] = ...) -> Any:
        spec = Schema.from_journal_dict(super().decode(s))
        return spec.to_journal_dict(JournalType.Private, None)
