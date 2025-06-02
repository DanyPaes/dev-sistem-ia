import pandas as pd

class RecomendadorHibrido:
    def __init__(self, modelo_colaborativo, modelo_conteudo, pesos=(0.5, 0.5)):
        """
        modelo_colaborativo: instância de RecomendacaoColaborativa (já preparada com .preparar())
        modelo_conteudo: instância de RecomendadorMaterial
        pesos: tupla (peso_colab, peso_conteudo)
        """
        self.colab = modelo_colaborativo
        self.conteudo = modelo_conteudo
        self.peso_colab, self.peso_conteudo = pesos

    def recomendar(self, id_aluno, texto_perfil_aluno, top_n=5):
        colab_recs = self.colab.recomendar_para(id_aluno, top_n=100)
        colab_recs = colab_recs.reset_index(drop=True)
        colab_recs['score_colab'] = [1.0 - i / 100 for i in range(len(colab_recs))]

        conteudo_recs = self.conteudo.recomendar(texto_perfil_aluno, top_n=100)
        conteudo_recs = conteudo_recs.rename(columns={'similaridade': 'score_conteudo'})

        # Merge incluindo titulo de ambos (para garantir título preenchido)
        df_merge = pd.merge(
            colab_recs[['id_material', 'titulo', 'score_colab']],
            conteudo_recs[['id_material', 'titulo', 'score_conteudo']],
            on='id_material',
            how='outer',
            suffixes=('_colab', '_conteudo')
        )

        # Combina títulos, priorizando título do colaborativo, se existir
        df_merge['titulo'] = df_merge['titulo_colab'].combine_first(df_merge['titulo_conteudo'])

        # Remove as colunas antigas de título
        df_merge = df_merge.drop(columns=['titulo_colab', 'titulo_conteudo'])

        df_merge['score_colab'] = df_merge['score_colab'].fillna(0)
        df_merge['score_conteudo'] = df_merge['score_conteudo'].fillna(0)

        df_merge['score_final'] = (
            self.peso_colab * df_merge['score_colab'] +
            self.peso_conteudo * df_merge['score_conteudo']
        )

        recomendados = df_merge.sort_values(by='score_final', ascending=False).head(top_n)

        return recomendados[['id_material', 'titulo', 'score_final']]
