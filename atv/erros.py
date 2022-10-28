from dataclasses import dataclass

from atv.mensagens import Mensagens


class Erro(Exception):
    def __init__(self, mensagem: str):
        self.mensagem = mensagem

    def __str__(self):
        return self.mensagem


@dataclass
class DescricaoVazia(Erro):
    mensagem: str = Mensagens.ERRO_DESCRICAO_NAO_PODE_SER_VAZIA.value
