class ContractModel:
    def __init__(self, id: str, version: str):
        self.id = id
        self.version = version


class SolidityModel(ContractModel):
    def __init__(self, version: str):
        super(SolidityModel, self).__init__("solidity", version)


solidity_one_oh = SolidityModel("1.0")

