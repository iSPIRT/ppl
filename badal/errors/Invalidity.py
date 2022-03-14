from typing import Dict, Any


class Invalidity:
    def __init__(self, code: str, attrs: Dict[str,Any]):
        self.code = code
        self.attrs = attrs