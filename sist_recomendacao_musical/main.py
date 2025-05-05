from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, List
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import numpy as np

app = FastAPI()
# Carregar dados
df = pd.read_csv("music.csv")

# Pré-processamento
df.columns = df.columns.str.split('-').str[0].str.strip()
df.rename(columns={'the genre of the track': 'genre'}, inplace=True)

data_users = {
    "01": ["Shape of You", "Perfect", "Thinking Out Loud"],
    "02": ["Blinding Lights", "Starboy", "Save Your Tears"],
    "03": ["Levitating", "Physical", "Don't Start Now"],
    "04": ["Someone Like You", "Hello", "Set Fire to the Rain"],
    "05": ["Bad Guy", "Ocean Eyes", "Therefore I Am"],
    "06": ["Bohemian Rhapsody", "We Are The Champions", "Somebody To Love"],
    "07": ["Stay", "Love Yourself", "Ghost"],
    "08": ["Uptown Funk", "24K Magic", "Treasure"],
    "09": ["Believer", "Radioactive", "Whatever It Takes"],
    "10": ["Dance Monkey", "Never Seen The Rain", "Fly Away"]
}


features = ['Beats.Per.Minute', 'Energy', 'Danceability',
'Loudness/dB',
'Liveness', 'Valence', 'Length', 'Acousticness',
'Speechiness', 'Popularity']

scaler = MinMaxScaler()
df[features] = scaler.fit_transform(df[features])


# Modelo de similaridade
similarity_matrix = cosine_similarity(df[features])
class GenreArtistRequest(BaseModel):
    genre: Optional[str] = None
    artist: Optional[str] = None
    limit: int = 5
class HybridRequest(BaseModel):
    song_title: str
    user_id: str
    content_weight: float = 0.7
    collab_weight: float = 0.3
    limit: int = 5


# Implementar os endpoints aqui...
#1
@app.get("/recommendations/content-based/{song_title}")
async def content_based_recommendations(song_title: str, limit: int =5, weights: Optional[Dict[str, float]] = None):
    if song_title not in df['title'].values:
        return "Essa música não está na base"

#2
@app.post("/recommendations/genre-artist", summary = "Genero/Artista")
async def genre_artist_recommendations(request: GenreArtistRequest):
    params = ['artist', 'limit', 'genre'] 
    valores = {
        param: None if str(getattr(request, param)).lower() in ['none', 'null', '', 'string'] else getattr(request, param)
        for param in params
    }

    artist = valores['artist']
    genre = valores['genre']
    limit = valores['limit']

    if artist is not None and genre is not None:
        musicas_filtradas = df[(df['artist'] == artist) & (df['genre'] == genre)]

    elif artist is not None:
        musicas_filtradas = df[df['artist'] == artist]

    elif genre is not None:
        musicas_filtradas = df[df['genre'] == genre]

    else:
        musicas_filtradas = df

    top_musicas = musicas_filtradas.nlargest(limit, 'Popularity')
    top_musicas = top_musicas[['title', 'artist', 'year', 'genre']]

    return top_musicas.to_dict(orient='records')

#3
@app.get("/recommendations/collaborative/{user_id}")
async def collaborative_recommendations(user_id: str, limit: int =5):
    all_songs = list({song for songs in data_users.values() for song in songs})

    df = pd.DataFrame(0, index=data_users.keys(), columns=all_songs)
    for user, songs in data_users.items():
        df.loc[user, songs] = 1

    if user_id not in df.index:
        return []

    matriz = cosine_similarity(df)
    df_sim = pd.DataFrame(matriz, index=df.index, columns=df.index)

    similares = df_sim[user_id].sort_values(ascending=False).drop(user_id)
    musicas_similares = set(df.loc[user_id][df.loc[user_id] == 1].index)
    ouvidas = set(df.columns[df.loc[user_id] == 1])

    recomendadas = []
    for similar_user in similares.index:
        for musica in df.columns[df.loc[similar_user] == 1]:
            if musica not in recomendadas:
                recomendadas.append(musica)

    recomendacoes = [musica for musica in recomendadas if musica not in ouvidas]

    return recomendacoes[:limit]

#4
@app.post("/recommendations/hybrid")
async def hybrid_recommendations(request: HybridRequest):
    """
Implementar recomendação híbrida
    """
    pass

#5
@app.get("/recommendations/popular", summary='Popularidade')
async def popular_recommendations(year: Optional[int] = None, genre: Optional[str] = None, limit: int = 5):
    if(year is not None and genre is not None):
        musicas = df[(df['year'] == year) & (df['genre'] == genre)]
        top_musicas = musicas.nlargest(limit, 'Popularity') 

        top_musicas = top_musicas[['title', 'artist', 'year', 'genre', 'Popularity']]

        return top_musicas.to_dict(orient='records')
    
    elif(year is not None):
        top_musicas = df[df['year'] == year].nlargest(limit, 'Popularity')
        top_musicas = top_musicas[['title', 'artist', 'year', 'genre', 'Popularity']]
        return top_musicas.to_dict(orient='records')
    
    elif(genre is not None):
        top_musicas = df[df['genre'] == genre].nlargest(limit, 'Popularity')
        top_musicas = top_musicas[['title', 'artist', 'year', 'genre', 'Popularity']]
        return top_musicas.to_dict(orient='records')

    else:
        top_musicas = df.nlargest(limit, 'Popularity')[['title', 'artist', 'year', 'genre']]
        return top_musicas.to_dict(orient='records')