import argparse
import pprint
from typing import Optional, Sequence


def comando_fazer():
    print("1 - checar se existe arquivo de tarefas para dia atual")
    print("2 - se não houver criar um, e escrever a data na primeira linha")
    print("3 - adicionar linha no final do arquivo com tarefa e status")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser_principal = argparse.ArgumentParser(prog="tdc")

    subparsers = parser_principal.add_subparsers(dest="comando", required=True)

    subparsers.add_parser(
        "fazer",
        help="adicionar uma nova atividade no dia atual"
    )

    args = parser_principal.parse_args(argv)

    pprint.pprint(vars(args))

    if args.comando == "fazer":
        return comando_fazer()
    else:
        raise NotImplementedError(f"Comando {args.comando} não implementado")


if __name__ == '__main__':
    exit(main())
