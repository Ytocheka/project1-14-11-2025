import random
import string
from typing import List


class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def generate_password(self, length: int = 12, use_lowercase: bool = True,
                          use_uppercase: bool = True, use_digits: bool = True,
                          use_special: bool = True) -> str:


        if length < 4:
            raise ValueError("Длина пароля должна быть не менее 4 символов")

        character_pool = ""

        if use_lowercase:
            character_pool += self.lowercase
        if use_uppercase:
            character_pool += self.uppercase
        if use_digits:
            character_pool += self.digits
        if use_special:
            character_pool += self.special_chars

        if not character_pool:
            raise ValueError("Должен быть выбран хотя бы один тип символов")

        password_chars = []

        if use_lowercase:
            password_chars.append(random.choice(self.lowercase))
        if use_uppercase:
            password_chars.append(random.choice(self.uppercase))
        if use_digits:
            password_chars.append(random.choice(self.digits))
        if use_special:
            password_chars.append(random.choice(self.special_chars))

        remaining_length = length - len(password_chars)
        if remaining_length > 0:
            password_chars.extend(random.choices(character_pool, k=remaining_length))

        random.shuffle(password_chars)

        return ''.join(password_chars)

    def generate_multiple(self, count: int, **kwargs) -> List[str]:
        return [self.generate_password(**kwargs) for _ in range(count)]
