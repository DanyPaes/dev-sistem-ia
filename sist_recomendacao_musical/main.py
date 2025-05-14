from fastapi import FastAPI, HTTPException, Path, Query, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, List
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import random

app = FastAPI()

# Carregar e limpar dados
df = pd.read_csv("music.csv")
df.columns = df.columns.str.split('-').str[0].str.strip()
df.rename(columns={'the genre of the track': 'genre'}, inplace=True)

# Normalizar features
features = ['Beats.Per.Minute', 'Energy', 'Danceability',
            'Loudness/dB', 'Liveness', 'Valence', 'Length',
            'Acousticness', 'Speechiness', 'Popularity']
scaler = MinMaxScaler()
df[features] = scaler.fit_transform(df[features])

# Gerador de usuários com músicas reais
titulos_musicas = df['title'].dropna().unique().tolist()
musicas_mais_populares = random.choices(titulos_musicas, k=25)

data_users = {}

for user_id in range(1, 201):
    total_musicas = random.randint(3, 10)

    musicas_usuario = random.sample(
        list(set(titulos_musicas) - set(musicas_mais_populares)),
        k=max(0, total_musicas - 3)
    ) + random.sample(musicas_mais_populares, k=min(3, total_musicas))

    random.shuffle(musicas_usuario)

    data_users[str(user_id)] = musicas_usuario


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
class SongResponse(BaseModel):
    title: str
    artist: str
    year: int
    genre: str

class Error(BaseModel):
    message: str
    detail: str

@app.post(
    "/recommendations/genre-artist",
    response_model=List[SongResponse],
    responses={
        200: {
            "description": "Recomendações filtradas por gênero e/ou artista",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "title": "Blinding Lights",
                            "artist": "The Weeknd",
                            "year": 2019,
                            "genre": "pop"
                        },
                        {
                            "title": "Starboy",
                            "artist": "The Weeknd",
                            "year": 2016,
                            "genre": "pop"
                        }
                    ]
                }
            }
        },
        422: {
            "model": Error,
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Erro de validação",
                        "detail": "Os campos fornecidos não estão no formato esperado."
                    }
                }
            }
        }
    },
    summary="Recomendações por Gênero/Artista",
    description=(
        "Retorna recomendações musicais com base em filtros por artista e/ou gênero. "
        "Caso nenhum filtro seja fornecido, retorna as músicas mais populares da base."
    )
)
async def genre_artist_recommendations(
    request: GenreArtistRequest = Body(
        ...,
        example={
            "artist": "Bruno Mars",
            "genre": "pop",
            "limit": 5
        }
    )
):
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
class RecomendacaoResponse(BaseModel):
    recomendacoes: List[str]

class Error(BaseModel):
    message: str
    detail: str

@app.get(
    "/recommendations/collaborative/{user_id}",
    response_model=RecomendacaoResponse,
    responses={
        200: {
            "description": "Recomendações geradas com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "recomendacoes": [
                            "Starboy",
                            "Save Your Tears",
                            "Blinding Lights"
                        ]
                    }
                }
            }
        },
        404: {
            "model": Error,
            "description": "Usuário não encontrado.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Usuário não encontrado",
                        "detail": "ID informado não está entre os usuários disponíveis."
                    }
                }
            },
        },
        422: {
            "model": Error,
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Erro de validação",
                        "detail": "O parâmetro user_id deve ser uma string válida."
                    }
                }
            },
        }
    },
    summary="Recomendações colaborativas",
    description="Recomenda músicas com base em similaridade entre usuários",
)
async def collaborative_recommendations(
    user_id: str = Path(example="101", description="ID do usuário para quem se deseja obter recomendações."),
    limit: int = Query(default=5, example=5, description="Quantidade máxima de recomendações a serem retornadas.")
):
    # Garante que não há músicas duplicadas na lista de todas as músicas
    all_songs = list({song for songs in data_users.values() for song in songs})
    df_temp = pd.DataFrame(0, index=data_users.keys(), columns=all_songs)

    for user, songs in data_users.items():
        musicas_unicas = list(set(songs))
        df_temp.loc[user, musicas_unicas] = 1

    if user_id not in df_temp.index:
        raise HTTPException(
            status_code=404,
            detail="ID informado não está entre os usuários disponíveis."
        )

    matriz = cosine_similarity(df_temp)
    df_sim = pd.DataFrame(matriz, index=df_temp.index, columns=df_temp.index)

    similares = df_sim[user_id].sort_values(ascending=False).drop(user_id)
    ouvidas = set(df_temp.columns[df_temp.loc[user_id] == 1])

    recomendadas = []
    for similar_user in similares.index:
        for musica in df_temp.columns[df_temp.loc[similar_user] == 1]:
            if musica not in recomendadas:
                recomendadas.append(musica)

    recomendacoes = [musica for musica in recomendadas if musica not in ouvidas]

    return {"recomendacoes": recomendacoes[:limit]}

#4
@app.post("/recommendations/hybrid")
async def hybrid_recommendations(request: HybridRequest):
    """
Implementar recomendação híbrida
    """
    pass

#5
class Musica(BaseModel):
    title: str
    artist: str
    year: int
    genre: str
    Popularity: float

class ListaMusicas(BaseModel):
    recomendacoes: List[Musica]

class Error(BaseModel):
    message: str
    detail: str

@app.get(
    "/recommendations/popular",
    response_model=List[Musica],
    responses={
        200: {
            "description": "Músicas mais populares retornadas com sucesso",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "title": "Blinding Lights",
                            "artist": "The Weeknd",
                            "year": 2020,
                            "genre": "pop",
                            "Popularity": 95
                        },
                        {
                            "title": "Levitating",
                            "artist": "Dua Lipa",
                            "year": 2020,
                            "genre": "pop",
                            "Popularity": 92
                        }
                    ]
                }
            }
        },
        422: {
            "model": Error,
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Erro de validação",
                        "detail": "O parâmetro year deve ser um número inteiro válido."
                    }
                }
            }
        }
    },
    summary="Recomendações por popularidade",
    description=(
        "Retorna as músicas mais populares com base no ano e/ou gênero informados. "
        "Se nenhum filtro for passado, retorna as mais populares de todos os tempos."
    )
)
async def popular_recommendations(
    year: Optional[int] = Query(
        default=None,
        example=2010,
        description="Filtrar por ano de lançamento das músicas."
    ),
    genre: Optional[str] = Query(
        default=None,
        example="dance pop",
        description="Filtrar por gênero musical das músicas."
    ),
    limit: int = Query(
        default=5,
        example=5,
        description="Quantidade máxima de músicas populares a serem retornadas."
    )
):
    try:
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

    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )
