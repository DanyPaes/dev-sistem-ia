import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Carregar o arquivo CSV
df = pd.read_csv("music.csv")

# Verificar as colunas do DataFrame


df.columns = df.columns.str.split('-').str[0].str.strip()
df.rename(columns={'the genre of the track': 'genre'}, inplace=True)

# Pré-processamento
print(df.columns)
features = ['Beats.Per.Minute', 'Energy', 'Danceability',
'Loudness/dB',
'Liveness', 'Valence', 'Length', 'Acousticness',
'Speechiness', 'Popularity']
scaler = MinMaxScaler()
df[features] = scaler.fit_transform(df[features])

print(df[features].head())

print(df.columns)
