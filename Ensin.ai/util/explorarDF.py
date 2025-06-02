def explorar_dataset(df):
    print("### Top 5 linhas:")
    print(df.head(), "\n")

    print("### Tipos das colunas:")
    print(df.dtypes, "\n")

    print("### Valores nulos por coluna:")
    print(df.isnull().sum(), "\n")

    print("### Estatísticas descritivas:")
    print(df.describe(), "\n")

    print("### Valores únicos por coluna:")
    for col in df.columns:
        print(f"- {col}: {df[col].unique()[:5]} ...")  # mostra só os 5 primeiros valores únicos
