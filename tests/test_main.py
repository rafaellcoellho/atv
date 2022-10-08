import argparse
from datetime import date

from tac.main import main, executa_comando, existe_arquivo_para_o_dia, obter_caminho_arquivo_do_dia


def test_comando_adicionar_atividade(tmp_path):
    hoje = date.today()
    caminho_pasta_arquivos = tmp_path

    codigo_de_erro = main(["adicionar", "tarefa exemplo"], caminho_pasta_arquivos)
    assert codigo_de_erro == 0

    assert existe_arquivo_para_o_dia(hoje, caminho_pasta_arquivos)

    caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(hoje, caminho_pasta_arquivos)
    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert len(linhas) == 1
        assert "tarefa exemplo" in linhas[0]


def test_comando_remover_atividade(tmp_path):
    hoje = date.today()
    caminho_pasta_arquivos = tmp_path

    main(["adicionar", "tarefa exemplo"], caminho_pasta_arquivos)

    caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(hoje, caminho_pasta_arquivos)
    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert len(linhas) == 1

    main(["remover", "0"], caminho_pasta_arquivos)

    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert len(linhas) == 0


def test_comando_concluir_atividade(tmp_path):
    hoje = date.today()
    caminho_pasta_arquivos = tmp_path

    main(["adicionar", "tarefa exemplo"], caminho_pasta_arquivos)

    caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(hoje, caminho_pasta_arquivos)
    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert len(linhas) == 1

    argumentos = argparse.Namespace(comando="concluir", indice=0)
    executa_comando(argumentos, caminho_pasta_arquivos)

    main(["concluir", "0"], caminho_pasta_arquivos)

    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert "concluida" in linhas[0]


def test_comando_desfazer_atividade(tmp_path):
    hoje = date.today()
    caminho_pasta_arquivos = tmp_path

    main(["adicionar", "tarefa exemplo"], caminho_pasta_arquivos)

    caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(hoje, caminho_pasta_arquivos)
    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert len(linhas) == 1

    main(["desfazer", "0"], caminho_pasta_arquivos)

    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert "pendente" in linhas[0]


def test_comando_listar_atividades(tmp_path, capsys):
    caminho_pasta_arquivos = tmp_path

    main(["listar"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "Não existe nenhuma tarefa nesse dia!" in resultado.out

    main(["adicionar", "tarefa exemplo"], caminho_pasta_arquivos)

    main(["listar"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "tarefa exemplo" in resultado.out
    assert "[ ]" in resultado.out
    assert "0" in resultado.out

    argumentos = argparse.Namespace(comando="concluir", indice=0)
    executa_comando(argumentos, caminho_pasta_arquivos)

    main(["concluir", "0"], caminho_pasta_arquivos)
    main(["listar"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "[v]" in resultado.out
