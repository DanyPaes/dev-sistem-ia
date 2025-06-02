# controllers/interacao_controller.py
from model.interacoes import carregar_interacoes

def listar_interacoes_por_aluno(id_aluno):
    interacoes = carregar_interacoes()
    return interacoes[interacoes['id_aluno'] == id_aluno].to_dict(orient='records')