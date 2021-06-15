from jwcrypto.jwk import JWK


def generate_keypair(key_id):
    return JWK(generate="EC", use="enc", kid=key_id)


