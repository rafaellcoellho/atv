import argparse
from datetime import date

from atv.main import (
    main,
    existe_arquivo_para_o_dia,
    obter_caminho_arquivo_do_dia,
)


def test_comando_adicionar_atividade(tmp_path):
    hoje = date.today()
    caminho_pasta_arquivos = str(tmp_path)

    codigo_de_erro = main(["a", "tarefa exemplo"], caminho_pasta_arquivos)
    assert codigo_de_erro == 0

    assert existe_arquivo_para_o_dia(hoje, caminho_pasta_arquivos)

    caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(
        hoje, caminho_pasta_arquivos
    )
    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert len(linhas) == 1
        assert "tarefa exemplo" in linhas[0]


def test_comando_remover_atividade(tmp_path):
    hoje = date.today()
    caminho_pasta_arquivos = str(tmp_path)

    main(["a", "tarefa exemplo"], caminho_pasta_arquivos)

    caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(
        hoje, caminho_pasta_arquivos
    )
    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert len(linhas) == 1

    main(["r", "0"], caminho_pasta_arquivos)

    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert len(linhas) == 0


def test_comando_concluir_atividade(tmp_path):
    hoje = date.today()
    caminho_pasta_arquivos = str(tmp_path)

    main(["a", "tarefa exemplo"], caminho_pasta_arquivos)

    caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(
        hoje, caminho_pasta_arquivos
    )
    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert len(linhas) == 1

    main(["c", "0"], caminho_pasta_arquivos)

    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert "concluida" in linhas[0]


def test_comando_desfazer_atividade(tmp_path):
    hoje = date.today()
    caminho_pasta_arquivos = str(tmp_path)

    main(["a", "tarefa exemplo"], caminho_pasta_arquivos)

    caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(
        hoje, caminho_pasta_arquivos
    )
    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert len(linhas) == 1

    main(["d", "0"], caminho_pasta_arquivos)

    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert "pendente" in linhas[0]


def test_comando_listar_atividades(tmp_path, capsys):
    caminho_pasta_arquivos = str(tmp_path)

    main(["l"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "Não existe nenhuma tarefa nesse dia!" in resultado.out

    main(["a", "tarefa exemplo"], caminho_pasta_arquivos)

    main(["l"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "tarefa exemplo" in resultado.out
    assert "[ ]" in resultado.out
    assert "0" in resultado.out

    main(["c", "0"], caminho_pasta_arquivos)
    main(["l"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "[v]" in resultado.out
