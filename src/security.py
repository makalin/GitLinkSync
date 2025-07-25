import os
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_value(value, key):
    f = Fernet(key)
    return f.encrypt(value.encode()).decode()

def decrypt_value(token, key):
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()

def get_secret(key, env_var=None):
    # Prefer environment variable, fallback to config
    return os.environ.get(env_var or key) 