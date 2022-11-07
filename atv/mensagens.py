from enum import Enum


class Mensagens(Enum):
    ERRO_DESCRICAO_NAO_PODE_SER_VAZIA = (
        "Atividade não adicionada, descrição não pode ser vazia."
    )
    ERRO_COMANDO_NAO_IMPLEMENTADO = "Comando não foi implementado."
    ERRO_REMOVER_ATIVIDADE_INEXISTENTE = (
        "A atividade nesse indice não existe para ser removida"
    )
    ERRO_CONCLUIR_ATIVIDADE_INEXISTENTE = (
        "A atividade nesse indice não existe para ser concluida"
    )
    ERRO_DESFAZER_ATIVIDADE_INEXISTENTE = (
        "A atividade nesse indice não existe para ser desfeita"
    )
    SUCESSO_ADICIONAR_ATIVIDADE = "Atividade foi adiciona com sucesso."
    SUCESSO_REMOVER_ATIVIDADE = "Atividade foi removida com sucesso"
    SUCESSO_CONCLUIR_ATIVIDADE = "Atividade foi concluida com sucesso"
    SUCESSO_DESFAZER_ATIVIDADE = "Atividade foi desfeita com sucesso"
