from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class RecomendadorMaterial:
    def __init__(self, materiais_df):
        """
        materiais_df: DataFrame com os materiais, que deve ter a coluna 'perfil_material' (texto unificado)
        """
        self.materiais = materiais_df.reset_index(drop=True)
        
        # Inicializa o vectorizer para TF-IDF
        # stop_words='english' remove palavras comuns sem muito significado
        # max_features limita a 2000 palavras mais importantes para o modelo
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=2000)
        
        # Gera a matriz TF-IDF dos materiais
        self.tfidf_materiais = self.vectorizer.fit_transform(self.materiais['perfil_material'])
    
    def vetor_perfil_aluno(self, texto_perfil):
        """
        Transforma o texto do perfil do aluno em vetor TF-IDF, usando o vectorizer já treinado.
        
        texto_perfil: string com o texto do perfil do aluno
        """
        return self.vectorizer.transform([texto_perfil])
    
    def recomendar(self, texto_perfil_aluno, top_n=5):
        """
        Recebe o texto do perfil do aluno e retorna os top_n materiais recomendados, com score de similaridade.
        
        texto_perfil_aluno: string com o texto do perfil do aluno
        top_n: quantos materiais recomendar (default 5)
        
        Retorna um DataFrame com as colunas: 'id_material', 'titulo', 'similaridade'
        """
        # Vetoriza o perfil do aluno
        vetor_aluno = self.vetor_perfil_aluno(texto_perfil_aluno)
        
        # Calcula similaridade do cosseno entre o perfil do aluno e todos os materiais
        similaridades = cosine_similarity(vetor_aluno, self.tfidf_materiais).flatten()
        
        # Pega os índices dos materiais com maior similaridade
        top_indices = similaridades.argsort()[-top_n:][::-1]
        
        # Seleciona os materiais recomendados e adiciona a coluna com o score
        recomendados = self.materiais.iloc[top_indices].copy()
        recomendados['similaridade'] = similaridades[top_indices]
        
        return recomendados[['id_material', 'titulo', 'similaridade']]

# Exemplo de uso (pode ficar em outro script ou na main):

if __name__ == "__main__":
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
    texto_perfil_primeiro_aluno = perfis_alunos.iloc[0]
    recomendados = recomendador.recomendar(texto_perfil_primeiro_aluno, top_n=5)

    print("Materiais recomendados para o primeiro aluno:")
    print(recomendados)
