from atv.main import main
from atv.mensagens import Mensagens


def limpar_stdout(capsys):
    capsys.readouterr()


def obter_linhas_do_stdout(stdout):
    linhas = stdout.split("\n")
    linhas_com_conteudo = [linha for linha in linhas if linha != ""]
    return linhas_com_conteudo


def test_comando_adicionar_atividade(tmp_path, capsys):
    caminho_pasta_arquivos = str(tmp_path)

    # adiciona o primeiro item
    main(["a", "tarefa 1"], caminho_pasta_arquivos)
    stdout = capsys.readouterr().out
    linhas = obter_linhas_do_stdout(stdout)
    assert len(linhas) == 2
    assert Mensagens.SUCESSO_ADICIONAR_ATIVIDADE.value == linhas[0]
    assert "tarefa 1" in linhas[1]
    assert "[ ]" in linhas[1]

    limpar_stdout(capsys)
    # adiciona o segundo item
    main(["a", "tarefa 2"], caminho_pasta_arquivos)
    stdout = capsys.readouterr().out
    linhas = obter_linhas_do_stdout(stdout)
    assert len(linhas) == 3
    assert Mensagens.SUCESSO_ADICIONAR_ATIVIDADE.value == linhas[0]
    assert "tarefa 1" in linhas[1]
    assert "[ ]" in linhas[1]
    assert "tarefa 2" in linhas[2]
    assert "[ ]" in linhas[2]

    limpar_stdout(capsys)
    # não permite adicionar descrição vazia
    main(["a", ""], caminho_pasta_arquivos)
    stdout = capsys.readouterr().out
    assert f"{str(Mensagens.ERRO_DESCRICAO_NAO_PODE_SER_VAZIA.value)}\n" == stdout


def test_comando_remover_atividade(tmp_path, capsys):
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
