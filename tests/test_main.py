from datetime import date

from atv.main import main


def test_comando_adicionar_atividade(tmp_path, capsys):
    caminho_pasta_arquivos = str(tmp_path)

    codigo_de_erro = main(["a", "tarefa exemplo"], caminho_pasta_arquivos)
    assert codigo_de_erro == 0

    main(["l"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "tarefa exemplo" in resultado.out
    assert "[ ]" in resultado.out


def test_comando_remover_atividade(tmp_path, capsys):
    hoje = date.today()
    caminho_pasta_arquivos = str(tmp_path)

    main(["a", "tarefa exemplo"], caminho_pasta_arquivos)

    main(["l"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "tarefa exemplo" in resultado.out

    main(["r", "0"], caminho_pasta_arquivos)

    main(["l"], caminho_pasta_arquivos)
    resultado = capsys.readouterr()
    assert "tarefa exemplo" not in resultado.out


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
