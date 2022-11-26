# atv

Aplicativo de linha comando para registrar atividades diárias.

<p align="center">
  <a href="https://raw.githubusercontent.com/rafaellcoellho/atv/blob/master/como_usar.gif">
		<img alt="como usar" src="como_usar.gif" width="600px">
	</a>
</p>

## Como usar

- `atv a <descrição>`: Adicionar uma nova atividade no dia atual
com a descrição informada;
- `atv r <indice>`: Remover uma atividade no dia atual, representada
pelo indice informado;
- `atv l` ou `atv`: Mostrar todas as atividades no dia atual;
- `atv c <indice>`: Marcar uma atividade no dia atual como concluída, selecionada
pelo indice informado;
- `atv d <indice>`: Marcar uma atividade no dia atual como pendente, selecionada
pelo indice informado;
- `atv --help`: Mostrar todos os comandos disponíveis.

Observações:

- Atividades são salvas como txt na pasta `/home/usuario_atual/.atv`;
- Todo dia um novo arquivo é criado.

## Desenvolvimento

#### Configurando ambiente local

Instalar versão do python. Eu utilizo o [asdf](https://asdf-vm.com/), com o plugin
[asdf-python](https://github.com/asdf-community/asdf-python) para fazer isso:

```
$ asdf install python 3.10.4
```

O arquivo `.tool-versions` vai reconhecer que nessa pasta utilizamos a versão correta:

```
$ python --version
Python 3.10.4
```

Crio e iniciar o ambiente virtual:

```
$ virtualenv venv
[...]
$ . venv/bin/activate
```

Instalar as dependências de desenvolvimento:

```
$ pip install -r requirements-dev.txt
```

Instalar a configuração do pre-commit:

```
$ pre-commit install
```

#### Como rodar testes

Rodar todos os ambientes de testes que tiver na sua máquina:

```
tox --skip-missing-interpreters
```

Rodar ambiente de teste especifico e teste especifico:

```
tox -e py310 -- tests/test_main.py::test_comando_adicionar_atividade
```

#### Como instalar

Construir os pacotes usando build:

```
python -m build
```

Instalar o pacote usando pip:

```
pip install dist/atv/atv-0.0.0.whl
```
