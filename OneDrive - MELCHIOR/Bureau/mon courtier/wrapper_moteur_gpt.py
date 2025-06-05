import json
from moteur_hybride_avec_fondamentaux import analyser_meilleure_opportunite


# 🔁 Fonction que l’API va appeler
def get_best_opportunity():
    try:
        with open("recommandation_top_1.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Si le fichier n’existe pas encore, on le crée
        resultat = analyser_meilleure_opportunite()
        with open("recommandation_top_1.json", "w", encoding="utf-8") as f_out:
            json.dump(resultat, f_out, ensure_ascii=False, indent=2)
        return resultat

# 🧪 Test local
if __name__ == "__main__":
    resultat = analyser_meilleure_opportunite()
    print(json.dumps(resultat, indent=2, ensure_ascii=False))

