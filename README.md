# tac

Aplicativo de linha comando para registrar atividades diárias.

## Como usar

- `tac adicionar <descrição>`: Adicionar uma nova atividade no dia atual
com a descrição informada;
- `tac remover <indice>`: Remover uma atividade no dia atual, representada
pelo indice informado;
- `tac listar` ou `tac`: Mostrar todas as atividades no dia atual;
- `tac concluir <indice>`: Marcar uma atividade no dia atual como concluída, selecionada
pelo indice informado;
- `tac desfazer <indice>`: Marcar uma atividade no dia atual como pendente, selecionada
pelo indice informado;
- `tac --help`: Mostrar todos os comandos disponíveis.

Observações:

- Atividades são salvas como txt na pasta `/home/usuario_atual/.tac`;
- Todo dia um novo arquivo é criado.

## Desenvolvimento

### Como rodar testes localmente

```commandline
virtualenv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

## Pendente

- [ ] `tac migrar <data>`: migrar todas as atividades não realizadas na data especificada
para o arquivo de hoje.
