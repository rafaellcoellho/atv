import argparse
import os
import pprint
from datetime import date
from typing import Optional, Sequence

CAMINHO_PASTA_ARQUIVOS = f"{os.getenv('HOME')}/.todo_app_cli"


def obter_caminho_arquivo_do_dia(dia: date) -> str:
    nome_do_arquivo = f"{dia.strftime('%Y-%m-%d')}.txt"
    caminho_para_arquivo = f"{CAMINHO_PASTA_ARQUIVOS}/{nome_do_arquivo}"

    return caminho_para_arquivo


def existe_pasta_de_arquivos() -> bool:
    return os.path.isdir(CAMINHO_PASTA_ARQUIVOS)


def escrever_tarefa_no_arquivo(descricao_tarefa: str, caminho_para_arquivo_dia_atual: str):
    with open(caminho_para_arquivo_dia_atual, "a+") as arquivo:
        arquivo.write(f"{descricao_tarefa} | pendente\n")


def ler_arquivo_de_tarefas(caminho_para_arquivo: str) -> list[str]:
    with open(caminho_para_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()

    return linhas


def comando_adicionar(descricao_tarefa: str) -> int:
    if not existe_pasta_de_arquivos():
        os.makedirs(CAMINHO_PASTA_ARQUIVOS)

    caminho_para_arquivo_dia_atual = obter_caminho_arquivo_do_dia(date.today())
    escrever_tarefa_no_arquivo(descricao_tarefa, caminho_para_arquivo_dia_atual)

    return 0


def comando_listar() -> int:
    if not existe_pasta_de_arquivos():
        print("Não existe nenhuma tarefa nesse dia!")
    else:
        caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(date.today())
        linhas = ler_arquivo_de_tarefas(caminho_para_arquivo_do_dia)

        for indice, linha in enumerate(linhas):
            descricao, situacao = linha.split("|")
            simbolo_situacao = "v" if "realizado" in situacao else " "
            print(f"{indice}. [{simbolo_situacao}] - {descricao}")

    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser_principal = argparse.ArgumentParser(prog="tac")

    subparsers = parser_principal.add_subparsers(dest="comando", required=True)

    parser_comando_adicionar = subparsers.add_parser(
        "adicionar",
        help="adicionar uma nova atividade no dia atual"
    )
    parser_comando_adicionar.add_argument("descricao", help="descrição da tarefa a ser feita")

    subparsers.add_parser(
        "listar",
        help="mostra todas as tarefas cadastradas no dia atual"
    )

    args = parser_principal.parse_args(argv)

    pprint.pprint(vars(args))

    if args.comando == "adicionar":
        return comando_adicionar(args.descricao)
    if args.comando == "listar":
        return comando_listar()
    else:
        raise NotImplementedError(f"Comando {args.comando} não implementado")


if __name__ == '__main__':
    exit(main())
