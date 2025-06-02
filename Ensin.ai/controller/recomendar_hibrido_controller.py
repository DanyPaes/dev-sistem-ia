# controllers/recomendacao_hibrida_controller.py
from models.recomendador_Hibrido import RecomendadorHibrido
from models.recomendador_SVD import RecomendacaoColaborativa
from models.recomendador_TFIDF import RecomendadorMaterial
from model.materiais_didaticos import carregar_materiais
from model.dados_alunos import carregar_alunos
from model.interacoes import carregar_interacoes
from model.perfil_aluno import gerar_perfis_aluno
from model.perfil_material import gerar_perfis_material

hibrido_model = None

def recomendar_hibrido(id_aluno, top_n=5):
    global hibrido_model

    materiais = carregar_materiais()
    if 'perfil_material' not in materiais.columns:
        materiais['perfil_material'] = gerar_perfis_material(materiais)

    alunos = carregar_alunos()
    perfil_aluno = gerar_perfis_aluno(alunos)[id_aluno]

    if hibrido_model is None:
        hibrido_model = RecomendadorHibrido(
            modelo_colaborativo=RecomendacaoColaborativa(
                df_interacoes=carregar_interacoes(),
                df_materiais=materiais
            ),
            modelo_conteudo=RecomendadorMaterial(materiais),
            pesos=(0.5, 0.5)
        )
        hibrido_model.colab.preparar()

    return hibrido_model.recomendar(id_aluno, perfil_aluno, top_n=top_n)
