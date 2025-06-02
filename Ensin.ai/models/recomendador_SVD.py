import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

class RecomendacaoColaborativa:
    def __init__(self, df_interacoes, df_materiais):
        self.df_interacoes = df_interacoes
        self.df_materiais = df_materiais
        self.matriz = None
        self.matriz_reduzida = None
        self.similaridade_alunos = None

    def preparar(self, n_components=5):
        # Cria a matriz aluno x material com avaliações
        self.matriz = self.df_interacoes.pivot_table(
            index='id_aluno',
            columns='id_material',
            values='avaliacao',
            fill_value=0
        )

        # Aplica SVD com n_components limitado pelas colunas da matriz
        n = min(n_components, self.matriz.shape[1] - 1)
        svd = TruncatedSVD(n_components=n, random_state=42)
        self.matriz_reduzida = svd.fit_transform(self.matriz)

        # Calcula similaridade entre alunos
        self.similaridade_alunos = cosine_similarity(self.matriz_reduzida)

    def recomendar_para(self, id_aluno, top_n=5):
        if self.similaridade_alunos is None:
            raise Exception("Chame o método preparar() antes de recomendar.")

        if id_aluno not in self.matriz.index:
            raise ValueError(f"Aluno {id_aluno} não encontrado.")

        idx = self.matriz.index.get_loc(id_aluno)
        similaridades = self.similaridade_alunos[idx]

        # Ordena por similaridade (ignora o próprio)
        usuarios_ordenados = np.argsort(similaridades)[::-1]
        usuarios_ordenados = usuarios_ordenados[usuarios_ordenados != idx]

        materiais_nao_vistos = self.matriz.iloc[idx][self.matriz.iloc[idx] == 0].index
        recomendados = {}

        for u_idx in usuarios_ordenados:
            materiais_vistos = self.matriz.iloc[u_idx][self.matriz.iloc[u_idx] > 0].index
            for m in materiais_vistos:
                if m in materiais_nao_vistos:
                    recomendados[m] = recomendados.get(m, 0) + similaridades[u_idx]
            if len(recomendados) >= top_n:
                break

        recomendados_ordenados = sorted(recomendados.items(), key=lambda x: x[1], reverse=True)
        ids_recomendados = [m[0] for m in recomendados_ordenados[:top_n]]

        return self.df_materiais[self.df_materiais['id_material'].isin(ids_recomendados)][['id_material', 'titulo']]

    # Alias para compatibilidade
    recomendar_por_usuarios_similares = recomendar_para
