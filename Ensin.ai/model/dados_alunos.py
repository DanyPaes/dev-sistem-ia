

def carregar_alunos():
    """
    Função para carregar o dataset de alunos.
    """
    import pandas as pd
    from util.explorarDF import explorar_dataset

    # Carregar o CSV
    df = pd.read_csv("data/dados_alunos_unicos.csv")
    
    
    return df

