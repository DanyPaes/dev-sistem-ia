import pandas as pd
from model.dados_alunos import carregar_alunos
from model.materiais_didaticos import carregar_materiais
from model.interacoes import carregar_interacoes

def carregar_dados():
    """
    Carrega os dados dos arquivos CSV.
    """
    interacoes = carregar_interacoes()
    materiais = carregar_materiais()
    return interacoes, materiais

def montar_matriz_aluno_item():
    interacoes = carregar_interacoes()
    if 'avaliacao' in interacoes.columns:
        matriz = interacoes.pivot_table(index='id_aluno', columns='id_material', values='avaliacao', fill_value=0)
    else:
        interacoes_copy = interacoes.copy()
        interacoes_copy['consumido'] = 1
        matriz = interacoes_copy.pivot_table(index='id_aluno', columns='id_material', values='consumido', fill_value=0)
    return matriz

