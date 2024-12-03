import random
import string


class PasswordGenerator:
    @staticmethod
    def generate(length: int = 12, use_digits: bool = True, use_uppercase: bool = True, 
                 use_lowercase: bool = True, use_special: bool = True) -> str:
        """
        Генерирует сложный пароль на основе указанных параметров.
        :param length: Длина пароля.
        :param use_digits: Использовать ли цифры.
        :param use_uppercase: Использовать ли заглавные буквы.
        :param use_lowercase: Использовать ли строчные буквы.
        :param use_special: Использовать ли специальные символы.
        :return: Сгенерированный пароль.
        """
        if length <= 0:
            raise ValueError("Длина пароля должна быть больше нуля.")

        character_pool = ""
        if use_digits:
            character_pool += string.digits
        if use_uppercase:
            character_pool += string.ascii_uppercase
        if use_lowercase:
            character_pool += string.ascii_lowercase
        if use_special:
            character_pool += "!@#$%^&*()-_=+[]{}|;:,.<>?/"

        if not character_pool:
            raise ValueError("Не выбран ни один набор символов для генерации пароля.")

        password = ''.join(random.choice(character_pool) for _ in range(length))
        return password


# Тестовый пример
if __name__ == "__main__":
    generator = PasswordGenerator()
    print("Сгенерированный пароль:", generator.generate(length=16, use_special=True))
