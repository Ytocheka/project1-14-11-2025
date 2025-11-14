import hashlib
import getpass
from typing import Optional


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def get_master_password() -> str:
    return getpass.getpass("Введите мастер-пароль: ")


def calculate_entropy(password: str) -> float:
    import math

    char_pool = 0
    if any(c.islower() for c in password):
        char_pool += 26
    if any(c.isupper() for c in password):
        char_pool += 26
    if any(c.isdigit() for c in password):
        char_pool += 10
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        char_pool += len("!@#$%^&*()_+-=[]{}|;:,.<>?")

    if char_pool == 0:
        return 0

    return len(password) * math.log2(char_pool)


def password_strength(password: str) -> str:
    entropy = calculate_entropy(password)

    if entropy < 28:
        return "Слабый"
    elif entropy < 36:
        return "Средний"
    elif entropy < 60:
        return "Сильный"
    else:
        return "Очень сильный"
