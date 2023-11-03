import base64
from hashlib import blake2b

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cryptography.hazmat.primitives import serialization as crypto_serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from django.conf import settings


def generate_keys():
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )
    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption()
    )
    public_key = key.public_key().public_bytes(
        encoding=crypto_serialization.Encoding.PEM,
        format=crypto_serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_key, public_key


def create_fernet(key: bytes, salt: bytes) -> Fernet:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(key))
    return Fernet(key)


def encrypt_text(text: str):
    fernet = create_fernet(settings.API_SECRET_KEY.encode(), settings.API_SALT.encode())
    encrypt_fernet = fernet.encrypt(text.encode())
    return base64.b64encode(encrypt_fernet).decode()


def decrypt_text(encoded_text: str):
    fernet = create_fernet(settings.API_SECRET_KEY.encode(), settings.API_SALT.encode())
    base = base64.b64decode(encoded_text)
    return fernet.decrypt(base).decode('utf8')


def load_public_key(public_key: bytes):
    return crypto_serialization.load_pem_public_key(public_key, backend=crypto_default_backend())


def load_private_key(private_key: bytes):
    return crypto_serialization.load_pem_private_key(private_key, password=None)


def decrypt(encoded_base64: str, private_key) -> str:
    encoded_bytes = base64.b64decode(encoded_base64)
    portions = []
    portion_size = 256

    portion = encoded_bytes[:portion_size]
    while portion:
        decrypted_portion = private_key.decrypt(
            portion,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        portions.append(decrypted_portion.decode())
        portion = encoded_bytes[portion_size * len(portions):portion_size * (len(portions) + 1)]

    return ''.join(portions)


def encrypt(data: bytes, public_key) -> str:
    portions = []
    portion_size = 190
    portion = data[:portion_size]
    while portion:
        encrypted_portion = public_key.encrypt(
            portion,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        portions.append(encrypted_portion)
        portion = data[len(portions) * portion_size:portion_size * (len(portions) + 1)]

    return base64.b64encode(b''.join(portions)).decode()


def get_hash(token: str, digest_size=64):
    return blake2b(
        token.encode('utf-8'),
        digest_size=digest_size,
        salt=settings.SALT.encode('utf-8'),
    ).hexdigest()
