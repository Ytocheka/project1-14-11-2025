import argparse
from typing import List
from .generator import PasswordGenerator
from .storage import PasswordStorage
from .utils import password_strength, get_master_password


def generate_command(args) -> None:
    generator = PasswordGenerator()

    try:
        if args.count > 1:
            passwords = generator.generate_multiple(
                count=args.count,
                length=args.length,
                use_lowercase=not args.no_lowercase,
                use_uppercase=not args.no_uppercase,
                use_digits=not args.no_digits,
                use_special=args.special
            )
            print(f"Сгенерировано {args.count} паролей:")
            for i, password in enumerate(passwords, 1):
                strength = password_strength(password)
                print(f"{i}. {password} [{strength}]")
        else:
            password = generator.generate_password(
                length=args.length,
                use_lowercase=not args.no_lowercase,
                use_uppercase=not args.no_uppercase,
                use_digits=not args.no_digits,
                use_special=args.special
            )
            strength = password_strength(password)
            print(f"Сгенерированный пароль: {password}")
            print(f"Сложность: {strength}")

        # Сохранение в файл если указано
        if args.save:
            storage = PasswordStorage()
            service = args.service or input("Введите название сервиса: ")
            username = args.username or input("Введите имя пользователя: ")
            master_password = get_master_password()

            if storage.store_password(service, username, password, master_password):
                print(f"Пароль для {service} успешно сохранен!")
            else:
                print("Ошибка: Неверный мастер-пароль!")

    except ValueError as e:
        print(f"Ошибка: {e}")


def search_command(args) -> None:
    storage = PasswordStorage()
    master_password = get_master_password()

    if args.service:
        # Поиск конкретного сервиса
        info = storage.retrieve_password_info(args.service, master_password)
        if info:
            print(f"Сервис: {info['service']}")
            print(f"Имя пользователя: {info['username']}")
            print("Пароль: [хранится в хэшированном виде]")
        else:
            print("Сервис не найден или неверный мастер-пароль")
    else:
        # Поиск по шаблону
        query = args.query or ""
        results = storage.search_passwords(query, master_password)

        if results:
            print(f"Найдено {len(results)} сервисов:")
            for result in results:
                print(f"- {result['service']} (пользователь: {result['username']})")
        else:
            print("Сервисы не найдены")


def list_command(args) -> None:
    storage = PasswordStorage()
    master_password = get_master_password()

    services = storage.list_services(master_password)

    if services:
        print(f"Сохранено {len(services)} сервисов:")
        for service in services:
            print(f"- {service}")
    else:
        print("Нет сохраненных сервисов или неверный мастер-пароль")


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Генератор безопасных паролей")
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")


    gen_parser = subparsers.add_parser("generate", help="Генерация паролей")
    gen_parser.add_argument("-l", "--length", type=int, default=12,
                            help="Длина пароля (по умолчанию: 12)")
    gen_parser.add_argument("--no-lowercase", action="store_true",
                            help="Исключить строчные буквы")
    gen_parser.add_argument("--no-uppercase", action="store_true",
                            help="Исключить заглавные буквы")
    gen_parser.add_argument("--no-digits", action="store_true",
                            help="Исключить цифры")
    gen_parser.add_argument("-s", "--special", action="store_true",
                            help="Включить специальные символы")
    gen_parser.add_argument("-c", "--count", type=int, default=1,
                            help="Количество генерируемых паролей")
    gen_parser.add_argument("--save", action="store_true",
                            help="Сохранить пароль в хранилище")
    gen_parser.add_argument("--service", type=str,
                            help="Название сервиса для сохранения")
    gen_parser.add_argument("--username", type=str,
                            help="Имя пользователя для сохранения")


    search_parser = subparsers.add_parser("search", help="Поиск сохраненных паролей")
    search_parser.add_argument("service", nargs="?", type=str,
                               help="Название сервиса для поиска")
    search_parser.add_argument("--query", type=str,
                               help="Поиск по шаблону")


    list_parser = subparsers.add_parser("list", help="Список всех сохраненных сервисов")

    return parser
