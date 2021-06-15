import decimal
import json
from typing import Any

from ppl.types.state import State, SerialisedState


class DineroEncoder(json.JSONEncoder):
    def default(self, o: Any) -> dict:
        if isinstance(o, State):
            json.JSONEncoder().encode(o.serialise())
        elif isinstance(o, SerialisedState):
            d = o.to_json()
            print(d)
            json.JSONEncoder().encode(d)
        elif isinstance(o, decimal.Decimal):
            return str(o)
        else:
            return json.JSONEncoder().encode(o)
