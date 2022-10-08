import argparse
from datetime import date

from main import executa_comando, existe_pasta_de_arquivos, existe_arquivo_para_o_dia, obter_caminho_arquivo_do_dia


def test_comando_adicionar_atividade(tmp_path):
    hoje = date.today()
    caminho_pasta_arquivos = tmp_path
    argumentos = argparse.Namespace(comando="adicionar", descricao="tarefa exemplo")

    executa_comando(argumentos, caminho_pasta_arquivos)

    assert existe_pasta_de_arquivos(caminho_pasta_arquivos)
    assert existe_arquivo_para_o_dia(hoje, caminho_pasta_arquivos)

    caminho_para_arquivo_do_dia = obter_caminho_arquivo_do_dia(hoje, caminho_pasta_arquivos)
    with open(caminho_para_arquivo_do_dia, "r") as arquivo:
        linhas = arquivo.readlines()
        assert len(linhas) == 1
        assert "tarefa exemplo" in linhas[0]
