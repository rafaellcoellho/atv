import argparse
import os
import pprint
from datetime import date
from typing import Optional, Sequence


def comando_fazer(descricao_tarefa: str) -> int:
    caminho_home_usuario_atual = os.getenv("HOME")
    caminho_pasta_arquivo_tarefas = f"{caminho_home_usuario_atual}/.todo_app_cli"
    existe_pasta_de_arquivos = os.path.isdir(caminho_pasta_arquivo_tarefas)

    if not existe_pasta_de_arquivos:
        os.makedirs(caminho_pasta_arquivo_tarefas)

    caminho_para_arquivo_dia_atual = f"{caminho_pasta_arquivo_tarefas}/{date.today().strftime('%Y-%m-%d')}.txt"

    with open(caminho_para_arquivo_dia_atual, "a+") as arquivo:
        arquivo.write(f"\n{descricao_tarefa} | pendente")

    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser_principal = argparse.ArgumentParser(prog="tdc")

    subparsers = parser_principal.add_subparsers(dest="comando", required=True)

    parser_comando_fazer = subparsers.add_parser(
        "fazer",
        help="adicionar uma nova atividade no dia atual"
    )
    parser_comando_fazer.add_argument("descricao", help="descrição da tarefa a ser feita")

    args = parser_principal.parse_args(argv)

    pprint.pprint(vars(args))

    if args.comando == "fazer":
        return comando_fazer(args.descricao)
    else:
        raise NotImplementedError(f"Comando {args.comando} não implementado")


if __name__ == '__main__':
    exit(main())
