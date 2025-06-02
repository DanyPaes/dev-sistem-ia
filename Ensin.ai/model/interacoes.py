def carregar_interacoes():
    """
    Função para carregar o dataset de interações.
    """
    import pandas as pd
    from util.explorarDF import explorar_dataset

    # Carregar o CSV
    df = pd.read_csv("data/interacoes_geradas.csv")

    # Explorar o dataset
    explorar_dataset(df)

    return df