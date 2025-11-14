#!/usr/bin/env python3

import sys
from passgen.commands import setup_parser, generate_command, search_command, list_command


def main():

    parser = setup_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "generate":
            generate_command(args)
        elif args.command == "search":
            search_command(args)
        elif args.command == "list":
            list_command(args)
        else:
            print(f"Неизвестная команда: {args.command}")
            parser.print_help()

    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
