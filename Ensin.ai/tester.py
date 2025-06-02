from model.dados_alunos import carregar_alunos
import pandas as pd
from models.recomendador_TFIDF import RecomendadorMaterial

def teste_TFIDF():
    # Supondo que você já tenha o DataFrame materiais e alunos carregados
    from model.dados_alunos import carregar_alunos
    from model.materiais_didaticos import carregar_materiais
    from model.perfil_aluno import gerar_perfis_aluno

    # Carrega dados
    materiais = carregar_materiais()
    alunos = carregar_alunos()

    # Gera perfil dos alunos (texto)
    perfis_alunos = gerar_perfis_aluno(alunos)

    # Cria a coluna com o perfil unificado no DataFrame de materiais
    # Aqui estou assumindo que você já tem o perfil_material nos materiais
    # Se não tiver, use a função que você criou para gerar
    if 'perfil_material' not in materiais.columns:
        from model.perfil_material import gerar_perfis_material
        materiais['perfil_material'] = gerar_perfis_material(materiais)

    # Inicializa o recomendador
    recomendador = RecomendadorMaterial(materiais)

    # Testa recomendação para o primeiro aluno
    texto_perfil_primeiro_aluno = perfis_alunos[1]
    recomendados = recomendador.recomendar(texto_perfil_primeiro_aluno, top_n=5)

    print("Materiais recomendados para o primeiro aluno:")
    print(recomendados)

def teste_SVD():
    from models.recomendador_SVD import RecomendacaoColaborativa

    from model.materiais_didaticos import carregar_materiais
    from model.interacoes import carregar_interacoes

    recom = RecomendacaoColaborativa(
        df_interacoes=carregar_interacoes(),
        df_materiais=carregar_materiais()
    )
    recom.preparar()  # carrega matriz, aplica SVD e calcula similaridades

    resultado = recom.recomendar_por_usuarios_similares(id_aluno=1, top_n=5)
    print(resultado)

def teste_hibrido():
    from models.recomendador_Hibrido import RecomendadorHibrido
    from models.recomendador_SVD import RecomendacaoColaborativa
    from model.materiais_didaticos import carregar_materiais
    from model.perfil_aluno import gerar_perfis_aluno
    from models.recomendador_TFIDF import RecomendadorMaterial
    from model.dados_alunos import carregar_alunos
    from model.perfil_aluno import gerar_perfis_aluno
    from model.interacoes import carregar_interacoes
    from model.perfil_material import gerar_perfis_material

    materiais = carregar_materiais()

    if 'perfil_material' not in materiais.columns:
        from model.perfil_material import gerar_perfis_material
        materiais['perfil_material'] = gerar_perfis_material(materiais)

    # Carrega os dados
    alunos = carregar_alunos()
    id_aluno = 1

    recomHibrido = RecomendadorHibrido(
        modelo_colaborativo=RecomendacaoColaborativa(
            df_interacoes=carregar_interacoes(),
            df_materiais=materiais
        ),
        modelo_conteudo=RecomendadorMaterial(materiais),
        pesos=(0.5, 0.5)
    )

    recomHibrido.colab.preparar()  # prepara o modelo colaborativo
    perfil_aluno = gerar_perfis_aluno(alunos)[id_aluno]
    recomendados = recomHibrido.recomendar(id_aluno, perfil_aluno, top_n=5)
    print("Recomendações híbridas:")
    print(recomendados)


def teste_metrics():
    id_aluno = 4
    from models.metrics import Metrics
    from models.recomendador_Hibrido import RecomendadorHibrido
    from models.recomendador_SVD import RecomendacaoColaborativa
    from model.materiais_didaticos import carregar_materiais
    from model.perfil_aluno import gerar_perfis_aluno
    from models.recomendador_TFIDF import RecomendadorMaterial
    from model.dados_alunos import carregar_alunos
    from model.interacoes import carregar_interacoes
    from model.perfil_material import gerar_perfis_material

    import numpy as np

    # Carrega os dados
    materiais = carregar_materiais()
    if 'perfil_material' not in materiais.columns:
        materiais['perfil_material'] = gerar_perfis_material(materiais)

    alunos = carregar_alunos()
    interacoes = carregar_interacoes()

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

    recomendados = recomHibrido.recomendar(id_aluno, perfil_aluno, top_n=5)
    relevantes = interacoes[interacoes['id_aluno'] == id_aluno]['id_material']

    metrics = Metrics(recomendados['id_material'].tolist(), relevantes.tolist(), k=5)

    print("Métricas Offline:")
    print(f"Precisão: {metrics.precision()}")
    print(f"Recall: {metrics.recall()}")
    print(f"F1-Score: {metrics.f1_score()}")

    # RMSE — exemplo com notas preditas aleatórias só pra demonstrar
    notas_reais = np.random.randint(1, 6, size=5)
    notas_preditas = np.random.uniform(1, 5, size=5)
    print(f"RMSE (exemplo aleatório): {Metrics.rmse(notas_preditas, notas_reais)}")

    # Coverage
    itens_recomendados_total = recomendados['id_material'].tolist()
    total_catalogo = len(materiais)
    print(f"Coverage: {Metrics.coverage(itens_recomendados_total, total_catalogo)}")

    # Diversity — usando os perfis de material como vetores
    perfis = [
        perfil for perfil in materiais.set_index('id_material')
        .loc[recomendados['id_material']]['perfil_material'].tolist()
        if isinstance(perfil, (list, np.ndarray))
    ]
    print(f"Diversity: {Metrics.diversity(perfis)}")


    


if __name__ == "__main__":
    teste_metrics()
    