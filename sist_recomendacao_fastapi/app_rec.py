from fastapi import FastAPI, HTTPException, Request
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

# Carregar os dados
ratings = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies.csv')

# Configuração do Jinja2 para renderizar templates HTML
templates = Jinja2Templates(directory="templates")

# 1. Função Best Seller | professor
def best_seller_recommendations_ratings(ratings, movies, top_n=10):
    movie_stats = ratings.groupby('movieId').agg(
        avg_rating=('rating', 'mean'),
        num_ratings=('rating', 'count')
    ).reset_index()

    min_ratings = 10
    movie_stats = movie_stats[movie_stats['num_ratings'] >= min_ratings]

    best_sellers = movie_stats.sort_values(by=['avg_rating', 'num_ratings'], ascending=[False, False])
    best_sellers = best_sellers.merge(movies, on='movieId')

    return best_sellers.head(top_n).to_dict(orient='records')

# best seller dany
def best_seller(top_n = 3):
  movies['qtd_assistido'] = movies['movieId'].map(ratings['movieId'].value_counts()).fillna(0).astype(int)
  bests_sellers = movies.nlargest(top_n, 'qtd_assistido')[['title', 'qtd_assistido']]

  return (bests_sellers
        .rename(columns={'qtd_assistido': 'Vezes assistidas', 'title': 'Título'})
        .to_dict(orient='records'))

# Endpoint para a página inicial
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoints FastAPI
@app.get("/best-seller/ratings/", tags=["Professor"], summary="Best Seller - Melhor avaliado", description="Calcula os Best Sellers com base na melhor média de notas")
async def get_best_seller_ratings(top_n: int = 10):
    return best_seller_recommendations_ratings(ratings, movies, top_n)

@app.get("/best-seller", tags=["Dany"], summary="Best Seller - Views", description="Calcula a quantidade de vezes em que cada filme foi visto e recomenda os mais assistidos")
async def get_best_seller(top_n: int = 3):
    return best_seller(top_n)

# Para rodar o FastAPI, use o comando: uvicorn app_rec:app --reload
#adicionando o uvicorn.run tava dando problema ao rodar da forma descrita acima, por isso retirei