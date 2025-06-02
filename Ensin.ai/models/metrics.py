import numpy as np
from sklearn.metrics import mean_squared_error
from itertools import combinations

class Metrics:
    def __init__(self, recomendados, relevantes, k=5):
        """
        recomendados: lista de ids recomendados (ordenados por score)
        relevantes: lista de ids que o usuário realmente considerou úteis
        k: quantidade de itens do top-K a considerar
        """
        self.k = k
        self.recomendados = recomendados[:k]
        self.relevantes = set(relevantes)

    def precision(self):
        acertos = sum([1 for item in self.recomendados if item in self.relevantes])
        return acertos / self.k if self.k > 0 else 0

    def recall(self):
        acertos = sum([1 for item in self.recomendados if item in self.relevantes])
        return acertos / len(self.relevantes) if self.relevantes else 0

    def f1_score(self):
        p = self.precision()
        r = self.recall()
        return 2 * p * r / (p + r) if p + r > 0 else 0

    @staticmethod
    def rmse(preditas, reais):
        """
        preditas: lista com as notas previstas
        reais: lista com as notas reais dadas pelo usuário
        """
        return np.sqrt(mean_squared_error(reais, preditas))

    @staticmethod
    def coverage(itens_recomendados_total, total_catalogo):
        """
        itens_recomendados_total: set ou lista de todos os ids recomendados no sistema (vários usuários)
        total_catalogo: número total de materiais no sistema
        """
        return len(set(itens_recomendados_total)) / total_catalogo if total_catalogo > 0 else 0

    @staticmethod
    def diversity(itens_com_features):
        """
        itens_com_features: lista de vetores de características (ex: embeddings de conteúdo)
        """
        if len(itens_com_features) < 2:
            return 0
        distancias = []
        for a, b in combinations(itens_com_features, 2):
            dist = np.linalg.norm(np.array(a) - np.array(b))
            distancias.append(dist)
        return np.mean(distancias) if distancias else 0
