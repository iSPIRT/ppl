from typing import Dict, Any


class GenericError(Exception):
    def __init__(self, code: str, attrs: Dict[str, Any]):
        self.code = code
        self.attrs = attrs