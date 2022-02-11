class ProofModel:
    def __init__(self, id: str, version: str):
        self.id = id
        self.version = version


class ZokratesModel(ProofModel):
    def __init__(self, version: str):
        super(ZokratesModel, self).__init__("zokrates", version)


zokrates_one_oh = ZokratesModel("1.0")

