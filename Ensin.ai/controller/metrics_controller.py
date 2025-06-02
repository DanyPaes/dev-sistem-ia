from models.metrics import Metrics
from models.recomendador_Hibrido import RecomendadorHibrido
from models.recomendador_SVD import RecomendacaoColaborativa
from models.recomendador_TFIDF import RecomendadorMaterial
from model.materiais_didaticos import carregar_materiais
from model.perfil_aluno import gerar_perfis_aluno
from model.dados_alunos import carregar_alunos
from model.interacoes import carregar_interacoes
from model.perfil_material import gerar_perfis_material
import numpy as np


def calcular_metricas_offline(id_aluno: int, top_n: int = 5):
    # Carrega os dados
    materiais = carregar_materiais()
    if 'perfil_material' not in materiais.columns:
        materiais['perfil_material'] = gerar_perfis_material(materiais)

    alunos = carregar_alunos()
    interacoes = carregar_interacoes()

    # Instancia recomendador híbrido
    recomHibrido = RecomendadorHibrido(
        modelo_colaborativo=RecomendacaoColaborativa(
            df_interacoes=interacoes,
            df_materiais=materiais
        ),
        modelo_conteudo=RecomendadorMaterial(materiais),
        pesos=(0.5, 0.5)
    )

    recomHibrido.colab.preparar()
    perfil_aluno = gerar_perfis_aluno(alunos)[id_aluno]

    # Gera recomendações
    recomendados = recomHibrido.recomendar(id_aluno, perfil_aluno, top_n=top_n)
    relevantes = interacoes[interacoes['id_aluno'] == id_aluno]['id_material']

    # Calcula métricas
    metrics = Metrics(recomendados['id_material'].tolist(), relevantes.tolist(), k=top_n)

    resultados = {
        "precisao": metrics.precision(),
        "recall": metrics.recall(),
        "f1_score": metrics.f1_score(),
        "rmse": 0,  # valor fixo
        "coverage": Metrics.coverage(recomendados['id_material'].tolist(), len(materiais)),
        "diversity": Metrics.diversity(
            [
                perfil for perfil in materiais.set_index('id_material')
                .loc[recomendados['id_material']]['perfil_material'].tolist()
                if isinstance(perfil, (list, np.ndarray))
            ]
        )
    }

    return resultados

def calcular_metricas_online():
    return {
        "ctr": 0,  # valor fixo
        "pesquisa": 0,  # valor fixo
        "engajamento": 0,  # valor fixo
    }