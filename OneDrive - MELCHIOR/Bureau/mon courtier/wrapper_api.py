from fastapi import FastAPI
from wrapper_moteur_gpt import get_best_opportunity

app = FastAPI()

@app.get("/recommandation")
def lire_recommandation():
    resultat = get_best_opportunity()
    return resultat
