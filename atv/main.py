import argparse
import os
import sys
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Sequence


CAMINHO_PASTA_ARQUIVOS = f"{os.getenv('HOME')}/.atv"


class Mensagens(Enum):
    ERRO_DESCRICAO_NAO_PODE_SER_VAZIA = (
        "Atividade não adicionada, descrição não pode ser vazia."
    )


class Erro(Exception):
    def __init__(self, mensagem: str):
        self.mensagem = mensagem

    def __str__(self):
        return self.mensagem


@dataclass
class DescricaoVazia(Erro):
    mensagem: str = Mensagens.ERRO_DESCRICAO_NAO_PODE_SER_VAZIA.value


def obter_caminho_arquivo_do_dia(dia: date, caminho_pasta_arquivos: str) -> str:
    nome_do_arquivo = f"{dia.strftime('%Y-%m-%d')}.txt"
    caminho_para_arquivo = f"{caminho_pasta_arquivos}/{nome_do_arquivo}"

    return caminho_para_arquivo


def existe_pasta_de_arquivos(caminho_pasta_arquivos: str) -> bool:
    return os.path.isdir(caminho_pasta_arquivos)


def existe_arquivo_para_o_dia(dia: date, caminho_pasta_arquivos: str) -> bool:
    return os.path.isfile(obter_caminho_arquivo_do_dia(dia, caminho_pasta_arquivos))


def escrever_tarefa_no_arquivo(
    descricao_tarefa: str, caminho_para_arquivo_dia_atual: str
):
    with open(caminho_para_arquivo_dia_atual, "a+") as arquivo:
        arquivo.write(f"{descricao_tarefa} | pendente\n")


def ler_arquivo_de_tarefas(caminho_para_arquivo: str) -> list[str]:
    with open(caminho_para_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()

    return linhas


def remover_linha_do_arquivo(caminho_para_arquivo: str, indice: int):
    with open(caminho_para_arquivo, "r+") as arquivo:
        linhas = arquivo.readlines()
        arquivo.seek(0)
        arquivo.truncate()

        for indice_do_arquivo, linha in enumerate(linhas):
            if indice_do_arquivo != int(indice):
                arquivo.write(linha)


def mudar_status_de_atividade(caminho_para_arquivo: str, indice: int, status: str):
    with open(caminho_para_arquivo, "r+") as arquivo:
        linhas = arquivo.readlines()
        arquivo.seek(0)
        arquivo.truncate()

        for indice_do_arquivo, linha in enumerate(linhas):
            if indice_do_arquivo == int(indice):
                descricao, _ = linha.split("|")
                arquivo.write(f"{descricao} | {status}\n")
            else:
                arquivo.write(linha)


def comando_adicionar(descricao_tarefa: str, caminho_pasta_arquivo: str) -> int:
    if not existe_pasta_de_arquivos(caminho_pasta_arquivo):
        os.makedirs(CAMINHO_PASTA_ARQUIVOS)

    descricao_eh_vazia = not descricao_tarefa.strip()
    if descricao_eh_vazia:
        raise DescricaoVazia

    caminho_para_arquivo_dia_atual = obter_caminho_arquivo_do_dia(
        date.today(), caminho_pasta_arquivo
    )
    escrever_tarefa_no_arquivo(descricao_tarefa, caminho_para_arquivo_dia_atual)

    return 0


def comando_listar(caminho_pasta_arquivos: str) -> int:
    if not existe_arquivo_para_o_dia(date.today(), caminho_pasta_arquivos):
        print("Não existe nenhuma tarefa nesse dia!")
    else:
        caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(
            date.today(), caminho_pasta_arquivos
        )
        linhas = ler_arquivo_de_tarefas(caminho_para_arquivo_do_dia)

        for indice, linha in enumerate(linhas):
            descricao, situacao = linha.split("|")
            simbolo_situacao = "v" if "concluida" in situacao else " "
            print(f"{indice}. [{simbolo_situacao}] - {descricao}")

    return 0


def comando_remover(indice: int, caminho_pasta_arquivos: str) -> int:
    if not existe_arquivo_para_o_dia(date.today(), caminho_pasta_arquivos):
        print("Não existe nenhuma tarefa nesse dia!")
    else:
        caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(
            date.today(), caminho_pasta_arquivos
        )
        remover_linha_do_arquivo(caminho_para_arquivo_do_dia, indice)

    return 0


def comando_concluir(indice: int, caminho_pasta_arquivos: str) -> int:
    if not existe_arquivo_para_o_dia(date.today(), caminho_pasta_arquivos):
        print("Não existe nenhuma tarefa nesse dia!")
    else:
        caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(
            date.today(), caminho_pasta_arquivos
        )
        mudar_status_de_atividade(caminho_para_arquivo_do_dia, indice, "concluida")

    return 0


def comando_desfazer(indice: int, caminho_pasta_arquivos: str) -> int:
    if not existe_arquivo_para_o_dia(date.today(), caminho_pasta_arquivos):
        print("Não existe nenhuma tarefa nesse dia!")
    else:
        caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(
            date.today(), caminho_pasta_arquivos
        )
        mudar_status_de_atividade(caminho_para_arquivo_do_dia, indice, "pendente")

    return 0


def executa_comando(argumentos: argparse.Namespace, caminho_pasta_arquivos: str) -> int:
    if argumentos.comando == "a":
        return comando_adicionar(argumentos.descricao, caminho_pasta_arquivos)
    elif argumentos.comando == "l":
        return comando_listar(caminho_pasta_arquivos)
    elif argumentos.comando == "r":
        return comando_remover(argumentos.indice, caminho_pasta_arquivos)
    elif argumentos.comando == "c":
        return comando_concluir(argumentos.indice, caminho_pasta_arquivos)
    elif argumentos.comando == "d":
        return comando_desfazer(argumentos.indice, caminho_pasta_arquivos)
    else:
        raise NotImplementedError(f"Comando {argumentos.comando} não implementado")


def main(
    argv: Sequence[str] | None = None,
    caminho_pasta_arquivos: str = CAMINHO_PASTA_ARQUIVOS,
) -> int:
    argumentos = argv if argv is not None else sys.argv[1:]
    parser_principal = argparse.ArgumentParser(prog="atv")

    subparsers = parser_principal.add_subparsers(dest="comando")

    # Adicionar
    parser_comando_adicionar = subparsers.add_parser(
        "a", help="adicionar uma nova atividade no dia atual"
    )
    parser_comando_adicionar.add_argument(
        "descricao", help="descrição da tarefa a ser feita"
    )

    # Listar
    subparsers.add_parser("l", help="mostra todas as tarefas cadastradas no dia atual")

    # Remover
    parser_comando_remover = subparsers.add_parser(
        "r", help="remover uma atividade no dia atual"
    )
    parser_comando_remover.add_argument(
        "indice", help="indice da tarefa a ser deletada"
    )

    # Concluir
    parser_comando_concluir = subparsers.add_parser(
        "c", help="concluir uma atividade no dia atual"
    )
    parser_comando_concluir.add_argument(
        "indice", help="indice da tarefa a ser deletada"
    )

    # Desfazer
    parser_comando_desfazer = subparsers.add_parser(
        "d", help="marcar uma atividade do dia atual como pendente"
    )
    parser_comando_desfazer.add_argument(
        "indice", help="indice da tarefa a ser selecionada como pendente"
    )

    if len(argumentos) == 0:
        argumentos = ["l"]
    argumentos_formatados = parser_principal.parse_args(argumentos)

    try:
        executa_comando(
            argumentos=argumentos_formatados,
            caminho_pasta_arquivos=caminho_pasta_arquivos,
        )
    except Erro as erro:
        print(erro.mensagem)
        return 1
    else:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
