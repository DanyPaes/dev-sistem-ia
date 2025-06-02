# controllers/recomendacao_colaborativa_controller.py
from models.recomendador_SVD import RecomendacaoColaborativa
from model.materiais_didaticos import carregar_materiais
from model.interacoes import carregar_interacoes

colab_model = None

def recomendar_por_colaborativo(id_aluno, top_n=5):
    global colab_model
    if colab_model is None:
        colab_model = RecomendacaoColaborativa(
            df_interacoes=carregar_interacoes(),
            df_materiais=carregar_materiais()
        )
        colab_model.preparar()
    return colab_model.recomendar_por_usuarios_similares(id_aluno=id_aluno, top_n=top_n)
