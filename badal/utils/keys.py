from Crypto.PublicKey.RSA import RsaKey


def key_to_hex(key: RsaKey) -> str:
    return bytes.hex(key.export_key(format="DER"))
