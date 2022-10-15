# atv

Aplicativo de linha comando para registrar atividades diárias.

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

#### Como rodar testes

Instalar tox globalmente se não tiver instalado:

```
pip install tox
```

Rodar todos os ambientes de testes que tiver na sua máquina:

```
tox --skip-missing-interpreters
```

Rodar ambiente de teste especifico e teste especifico:

```
tox -e py310 -- tests/test_main.py::test_comando_adicionar_atividade
```

#### Como instalar

Instalar ferramenta de build usando pip:

```
pip install build
```

Construir os pacotes usando build:

```
python -m build
```

Instalar o pacote usando pip:

```
pip install dist/atv/atv-0.0.0.whl
```

## Pendente

- [ ] `atv m <data>`: migrar todas as atividades não realizadas na data especificada
para o arquivo de hoje.
