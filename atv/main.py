import argparse
import os
import sys
from datetime import date
from typing import Sequence

from atv import __version__
from atv.erros import (
    DescricaoVazia,
    Erro,
    ComandoNaoImplementado,
    RemoverAtividadeInexistente,
    ConcluirAtividadeInexistente,
    DesfazerAtividadeInexistente,
    DescricaoComQuebraDeLinha,
)
from atv.mensagens import Mensagens

CAMINHO_PASTA_ARQUIVOS = f"{os.getenv('HOME')}/.atv"


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


def nao_existe_indice_no_arquivo(indice: int, linhas: list[str]) -> bool:
    quantidade_de_linhas: int = len(linhas)
    return indice + 1 > quantidade_de_linhas


def remover_linha_do_arquivo(caminho_para_arquivo: str, indice: int):
    with open(caminho_para_arquivo, "r+") as arquivo:
        linhas = arquivo.readlines()
        arquivo.seek(0)
        arquivo.truncate()

        if nao_existe_indice_no_arquivo(int(indice), linhas):
            raise RemoverAtividadeInexistente

        for indice_do_arquivo, linha in enumerate(linhas):
            if indice_do_arquivo != int(indice):
                arquivo.write(linha)


def mudar_status_de_atividade(caminho_para_arquivo: str, indice: int, status: str):
    with open(caminho_para_arquivo, "r+") as arquivo:
        linhas = arquivo.readlines()
        arquivo.seek(0)
        arquivo.truncate()

        if nao_existe_indice_no_arquivo(int(indice), linhas):
            if status == "concluida":
                raise ConcluirAtividadeInexistente
            else:
                raise DesfazerAtividadeInexistente

        for indice_do_arquivo, linha in enumerate(linhas):
            if indice_do_arquivo == int(indice):
                descricao, _ = linha.split("|")
                arquivo.write(f"{descricao} | {status}\n")
            else:
                arquivo.write(linha)


def comando_adicionar(descricao_tarefa: str, caminho_pasta_arquivo: str):
    if not existe_pasta_de_arquivos(caminho_pasta_arquivo):
        os.makedirs(CAMINHO_PASTA_ARQUIVOS)

    descricao_eh_vazia = not descricao_tarefa.strip()
    if descricao_eh_vazia:
        raise DescricaoVazia

    descricao_contem_quebra_de_linha = "\n" in descricao_tarefa
    if descricao_contem_quebra_de_linha:
        raise DescricaoComQuebraDeLinha

    caminho_para_arquivo_dia_atual = obter_caminho_arquivo_do_dia(
        date.today(), caminho_pasta_arquivo
    )
    escrever_tarefa_no_arquivo(descricao_tarefa, caminho_para_arquivo_dia_atual)

    print(Mensagens.SUCESSO_ADICIONAR_ATIVIDADE.value)


def comando_listar(caminho_pasta_arquivos: str, mostrar_mensagens: bool = False):
    if not existe_arquivo_para_o_dia(date.today(), caminho_pasta_arquivos):
        if mostrar_mensagens:
            print(Mensagens.NAO_EXISTE_ATIVIDADES_PARA_LISTAR.value)
        return

    caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(
        date.today(), caminho_pasta_arquivos
    )
    linhas = ler_arquivo_de_tarefas(caminho_para_arquivo_do_dia)

    if len(linhas) == 0:
        if mostrar_mensagens:
            print(Mensagens.NAO_EXISTE_ATIVIDADES_PARA_LISTAR.value)
        return

    for indice, linha in enumerate(linhas):
        descricao, situacao = linha.split("|")
        simbolo_situacao = "v" if "concluida" in situacao else " "
        print(f"{indice}. [{simbolo_situacao}] - {descricao}")


def comando_remover(indice: int, caminho_pasta_arquivos: str):
    if not existe_arquivo_para_o_dia(date.today(), caminho_pasta_arquivos):
        raise RemoverAtividadeInexistente

    caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(
        date.today(), caminho_pasta_arquivos
    )
    remover_linha_do_arquivo(caminho_para_arquivo_do_dia, indice)

    print(Mensagens.SUCESSO_REMOVER_ATIVIDADE.value)


def comando_concluir(indice: int, caminho_pasta_arquivos: str):
    if not existe_arquivo_para_o_dia(date.today(), caminho_pasta_arquivos):
        raise ConcluirAtividadeInexistente

    caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(
        date.today(), caminho_pasta_arquivos
    )
    mudar_status_de_atividade(caminho_para_arquivo_do_dia, indice, "concluida")

    print(Mensagens.SUCESSO_CONCLUIR_ATIVIDADE.value)


def comando_desfazer(indice: int, caminho_pasta_arquivos: str):
    if not existe_arquivo_para_o_dia(date.today(), caminho_pasta_arquivos):
        raise DesfazerAtividadeInexistente

    caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(
        date.today(), caminho_pasta_arquivos
    )
    mudar_status_de_atividade(caminho_para_arquivo_do_dia, indice, "pendente")

    print(Mensagens.SUCESSO_DESFAZER_ATIVIDADE.value)


def executa_comando(argumentos: argparse.Namespace, caminho_pasta_arquivos: str) -> int:
    if argumentos.comando == "a":
        comando_adicionar(argumentos.descricao, caminho_pasta_arquivos)
        comando_listar(caminho_pasta_arquivos)
    elif argumentos.comando == "l":
        comando_listar(caminho_pasta_arquivos, mostrar_mensagens=True)
    elif argumentos.comando == "r":
        comando_remover(argumentos.indice, caminho_pasta_arquivos)
        comando_listar(caminho_pasta_arquivos)
    elif argumentos.comando == "c":
        comando_concluir(argumentos.indice, caminho_pasta_arquivos)
        comando_listar(caminho_pasta_arquivos)
    elif argumentos.comando == "d":
        comando_desfazer(argumentos.indice, caminho_pasta_arquivos)
        comando_listar(caminho_pasta_arquivos)
    else:
        raise ComandoNaoImplementado

    return 0


def main(
    argv: Sequence[str] | None = None,
    caminho_pasta_arquivos: str = CAMINHO_PASTA_ARQUIVOS,
) -> int:
    argumentos = argv if argv is not None else sys.argv[1:]
    parser_principal = argparse.ArgumentParser(
        prog="atv",
        description="Aplicativo de linha de comando para registrar atividades diárias",
        epilog="Autor: Rafael Coelho (rafaellcoellho@gmail.com)",
    )

    versao = f"{__version__}"
    parser_principal.add_argument(
        "--version",
        action="version",
        version=versao,
        help="mostra versão do aplicativo",
    )

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
        return erro.codigo_de_status
    else:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
