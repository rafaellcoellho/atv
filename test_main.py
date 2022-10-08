import argparse
from datetime import date

from main import executa_comando, existe_pasta_de_arquivos, existe_arquivo_para_o_dia, obter_caminho_arquivo_do_dia


def test_comando_adicionar_atividade(tmp_path):
    hoje = date.today()
    caminho_pasta_arquivos = tmp_path
    argumentos = argparse.Namespace(comando="adicionar", descricao="tarefa exemplo")

    executa_comando(argumentos, caminho_pasta_arquivos)

    assert existe_arquivo_para_o_dia(hoje, caminho_pasta_arquivos)

    caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(hoje, caminho_pasta_arquivos)
    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert len(linhas) == 1
        assert "tarefa exemplo" in linhas[0]


def test_comando_remover_atividade(tmp_path):
    hoje = date.today()
    caminho_pasta_arquivos = tmp_path

    argumentos = argparse.Namespace(comando="adicionar", descricao="tarefa exemplo")
    executa_comando(argumentos, caminho_pasta_arquivos)

    caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(hoje, caminho_pasta_arquivos)
    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert len(linhas) == 1

    argumentos = argparse.Namespace(comando="remover", indice=0)
    executa_comando(argumentos, caminho_pasta_arquivos)

    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert len(linhas) == 0


def test_comando_concluir_atividade(tmp_path):
    hoje = date.today()
    caminho_pasta_arquivos = tmp_path

    argumentos = argparse.Namespace(comando="adicionar", descricao="tarefa exemplo")
    executa_comando(argumentos, caminho_pasta_arquivos)

    caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(hoje, caminho_pasta_arquivos)
    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert len(linhas) == 1

    argumentos = argparse.Namespace(comando="concluir", indice=0)
    executa_comando(argumentos, caminho_pasta_arquivos)

    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert "concluida" in linhas[0]


def test_comando_desfazer_atividade(tmp_path):
    hoje = date.today()
    caminho_pasta_arquivos = tmp_path

    argumentos = argparse.Namespace(comando="adicionar", descricao="tarefa exemplo")
    executa_comando(argumentos, caminho_pasta_arquivos)

    caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(hoje, caminho_pasta_arquivos)
    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert len(linhas) == 1

    argumentos = argparse.Namespace(comando="desfazer", indice=0)
    executa_comando(argumentos, caminho_pasta_arquivos)

    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert "pendente" in linhas[0]


def test_comando_listar_atividades(tmp_path, capsys):
    caminho_pasta_arquivos = tmp_path

    argumentos = argparse.Namespace(comando="listar")
    executa_comando(argumentos, caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "Não existe nenhuma tarefa nesse dia!" in resultado.out

    argumentos = argparse.Namespace(comando="adicionar", descricao="tarefa exemplo")
    executa_comando(argumentos, caminho_pasta_arquivos)

    argumentos = argparse.Namespace(comando="listar")
    executa_comando(argumentos, caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "tarefa exemplo" in resultado.out
    assert "[ ]" in resultado.out
    assert "0" in resultado.out

    argumentos = argparse.Namespace(comando="concluir", indice=0)
    executa_comando(argumentos, caminho_pasta_arquivos)

    argumentos = argparse.Namespace(comando="listar")
    executa_comando(argumentos, caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "[v]" in resultado.out
