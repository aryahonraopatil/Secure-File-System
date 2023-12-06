from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend

# Diffie-Hellman Key Exchange:
def generate_key_pair():
    parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

# Generate keys for each peer
private_key_peer1, public_key_peer1 = generate_key_pair()
private_key_peer2, public_key_peer2 = generate_key_pair()