import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings


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
