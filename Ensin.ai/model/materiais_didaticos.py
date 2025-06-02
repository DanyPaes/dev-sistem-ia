def carregar_materiais():
    """
    Função para carregar o dataset de materiais didáticos.
    """
    import pandas as pd
    from util.explorarDF import explorar_dataset

    # Carregar o CSV
    df = pd.read_csv("data/materiais_didaticos_unicos.csv")

    # Explorar o dataset
    explorar_dataset(df)

    return df