from enum import Enum


class Mensagens(Enum):
    ERRO_DESCRICAO_NAO_PODE_SER_VAZIA = (
        "Atividade não adicionada, descrição não pode ser vazia."
    )
    ERRO_COMANDO_NAO_IMPLEMENTADO = "Comando não foi implementado."
