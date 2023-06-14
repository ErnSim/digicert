import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def generate_key_pair():
    with open("random.txt", "rb") as file:
        random_data = file.read()

    digest = hashes.Hash(hashes.SHA256())
    digest.update(random_data)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    with open("public_key.pem", "wb") as file:
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        file.write(public_key_pem)

    return private_key, public_key


def sign_file(file_path, private_key):
    with open(file_path, "rb") as file:
        data = file.read()

    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    hashed_data = digest.finalize()

    signature = private_key.sign(
        hashed_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature


def save_signature(signature):
    with open("signature.txt", "wb") as file:
        file.write(signature)


def load_signature():
    with open("signature.txt", "rb") as file:
        signature = file.read()

    return signature


def verify_signature(file_path, signature, public_key):
    with open(file_path, "rb") as file:
        data = file.read()

    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    hashed_data = digest.finalize()

    try:
        public_key.verify(
            signature,
            hashed_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Podpis cyfrowy jest poprawny.")
    except:
        print("Podpis cyfrowy jest niepoprawny.")
