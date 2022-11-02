from dataclasses import dataclass

from atv.mensagens import Mensagens


class Erro(Exception):
    def __init__(self, mensagem: str, codigo_de_status: int):
        self.mensagem = mensagem
        self.codigo_de_status = codigo_de_status

    def __str__(self):
        return self.mensagem


@dataclass
class DescricaoVazia(Erro):
    mensagem: str = Mensagens.ERRO_DESCRICAO_NAO_PODE_SER_VAZIA.value
    codigo_de_status: int = 1


@dataclass
class ComandoNaoImplementado(Erro):
    mensagem: str = Mensagens.ERRO_COMANDO_NAO_IMPLEMENTADO.value
    codigo_de_status: int = 1


@dataclass
class RemoverAtividadeInexistente(Erro):
    mensagem: str = Mensagens.ERRO_REMOVER_ATIVIDADE_INEXISTENTE.value
    codigo_de_status: int = 1
