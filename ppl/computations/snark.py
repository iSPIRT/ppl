import hashlib
from pysnark.runtime import snark

@snark
def hash(x: str):
    return hashlib.sha256(x.encode("utf-8")).hexdigest()

if __name__ == "__main__":
    digest = hash("a quick brown fox jumped over the lazy dog")
    print(digest)
