import argparse
from datetime import date

from atv.main import main, Mensagens


def test_comando_adicionar_atividade(tmp_path, capsys):
    caminho_pasta_arquivos = str(tmp_path)

    codigo_de_erro = main(["a", "tarefa exemplo"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert codigo_de_erro == 0
    assert str(Mensagens.SUCESSO_ADICIONA_ATIVIDADE.value) in resultado.out
    assert "tarefa exemplo" in resultado.out
    assert "[ ]" in resultado.out


def test_comando_remover_atividade(tmp_path, capsys):
    caminho_pasta_arquivos = str(tmp_path)

    main(["r", "0"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert str(Mensagens.NENHUMA_ATIVIDADE.value) in resultado.out

    main(["a", "tarefa exemplo"], caminho_pasta_arquivos)

    # tenta remover uma atividade que não existe mesmo já existindo atividade
    main(["r", "1"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert str(Mensagens.NENHUMA_ATIVIDADE.value) in resultado.out

    main(["r", "0"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert str(Mensagens.SUCESSO_REMOVER_ATIVIDADE.value) in resultado.out
    assert "tarefa exemplo" not in resultado.out

    # remove novamente quando não tem mais nenhuma atividade
    main(["r", "0"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert str(Mensagens.SUCESSO_REMOVER_ATIVIDADE.value) in resultado.out


def test_comando_concluir_atividade(tmp_path, capsys):
    caminho_pasta_arquivos = str(tmp_path)

    main(["a", "tarefa exemplo"], caminho_pasta_arquivos)

    main(["l"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "tarefa exemplo" in resultado.out
    assert "[ ]" in resultado.out

    main(["c", "0"], caminho_pasta_arquivos)

    main(["l"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "tarefa exemplo" in resultado.out
    assert "[v]" in resultado.out


def test_comando_desfazer_atividade(tmp_path, capsys):
    caminho_pasta_arquivos = str(tmp_path)

    main(["a", "tarefa exemplo"], caminho_pasta_arquivos)
    main(["c", "0"], caminho_pasta_arquivos)

    main(["l"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "tarefa exemplo" in resultado.out
    assert "[v]" in resultado.out

    main(["d", "0"], caminho_pasta_arquivos)

    main(["l"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "tarefa exemplo" in resultado.out
    assert "[ ]" in resultado.out


def test_comando_listar_atividades(tmp_path, capsys):
    caminho_pasta_arquivos = str(tmp_path)

    main(["a", "tarefa exemplo"], caminho_pasta_arquivos)

    main(["l"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "tarefa exemplo" in resultado.out
    assert "[ ]" in resultado.out
    assert "0" in resultado.out


def test_listar_sem_usar_comando(tmp_path, capsys):
    caminho_pasta_arquivos = str(tmp_path)

    main([], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "Não existe nenhuma tarefa nesse dia!" in resultado.out

    main(["a", "tarefa exemplo"], caminho_pasta_arquivos)

    main([], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "tarefa exemplo" in resultado.out
    assert "[ ]" in resultado.out
    assert "0" in resultado.out


def test_comando_listar_sem_atividades(tmp_path, capsys):
    caminho_pasta_arquivos = str(tmp_path)

    main(["l"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert str(Mensagens.NENHUMA_ATIVIDADE.value) in resultado.out

    # agora adiciona uma atividade e depois remove e checa se mostra a mensagem mesmo assim
    main(["a", "tarefa exemplo"], caminho_pasta_arquivos)
    main(["r", "0"], caminho_pasta_arquivos)

    main(["l"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert str(Mensagens.NENHUMA_ATIVIDADE.value) in resultado.out
