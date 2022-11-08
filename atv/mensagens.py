from enum import Enum


class Mensagens(Enum):
    ERRO_DESCRICAO_NAO_PODE_SER_VAZIA = (
        "Atividade não adicionada, descrição não pode ser vazia"
    )
    ERRO_DESCRICAO_NAO_PODE_CONTER_QUEBRA_DE_LINHA = (
        "Atividade não adiciona, descrição não pode conter quebra de linha"
    )
    ERRO_COMANDO_NAO_IMPLEMENTADO = "Comando não foi implementado"
    ERRO_REMOVER_ATIVIDADE_INEXISTENTE = (
        "A atividade nesse indice não existe para ser removida"
    )
    ERRO_CONCLUIR_ATIVIDADE_INEXISTENTE = (
        "A atividade nesse indice não existe para ser concluida"
    )
    ERRO_DESFAZER_ATIVIDADE_INEXISTENTE = (
        "A atividade nesse indice não existe para ser desfeita"
    )
    NAO_EXISTE_ATIVIDADES_PARA_LISTAR = "Não existe atividade para mostrar nesse dia"
    SUCESSO_ADICIONAR_ATIVIDADE = "Atividade foi adiciona com sucesso"
    SUCESSO_REMOVER_ATIVIDADE = "Atividade foi removida com sucesso"
    SUCESSO_CONCLUIR_ATIVIDADE = "Atividade foi concluida com sucesso"
    SUCESSO_DESFAZER_ATIVIDADE = "Atividade foi desfeita com sucesso"
