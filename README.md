# tac

Aplicativo de linha comando para registrar atividades diárias.

## Como usar

- [x] `tac adicionar <descrição>`: Adicionar uma nova atividade no dia atual
com a descrição informada;
- [x] `tac remover <indice>`: Remover uma atividade no dia atual, representada
pelo indice informado;
- [x] `tac listar` ou `tac`: Mostrar todas as atividades no dia atual;
- [x] `tac concluir <indice>`: Marcar uma atividade no dia atual como concluída, selecionada
pelo indice informado;
- [x] `tac desfazer <indice>: Marcar uma atividade no dia atual como pendente, selecionada
pelo indice informado;
- [x] `tac --help`: Mostrar todos os comandos disponíveis.

Observações:

- [x] Atividades são salvas como txt na pasta `/home/usuario_atual/.tac`;
- [x] Todo dia um novo arquivo é criado.

## Pendente

- [ ] `tac migrar <data>`: migrar todas as atividades não realizadas na data especificada
para o arquivo de hoje.
