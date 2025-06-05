import os
import json
import pandas as pd
import requests
import numpy as np
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("EODHD_API_KEY")
BASE_URL = "https://eodhistoricaldata.com/api"

def get_rsi(data, period=14):
    if len(data) < period:
        return None
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def get_fundamentals(symbol):
    url = f"{BASE_URL}/fundamentals/{symbol}?api_token={API_KEY}"
    try:
        r = requests.get(url)
        data = r.json()

        # Extraction des indicateurs fondamentaux
        profitability = float(data.get("Highlights", {}).get("GrossMarginTTM", 0)) * 100
        stability = float(data.get("Valuation", {}).get("DebtEquity", 0))
        growth = float(data.get("Highlights", {}).get("RevenueGrowthTTM", 0)) * 100

        # Pondération des scores
        score = 0.6 * profitability + 0.3 * (100 - stability) + 0.1 * growth
        return round(score, 2)

    except Exception as e:
        print(f"Erreur fonda {symbol} : {e}")
        return 0

def analyser_meilleure_opportunite():
    resultats = [analyse_action(row) for _, row in df.iterrows()]
    resultats = [res for res in resultats if res is not None]
    resultats = sorted(resultats, key=lambda x: x["score_total"], reverse=True)

    if resultats:
        top = resultats[0]
        with open("recommandation_top_1.json", "w", encoding="utf-8") as f:
            json.dump(top, f, ensure_ascii=False, indent=2)
        return top
    else:
        return None

if __name__ == "__main__":
    top = analyser_meilleure_opportunite()
    if top:
        print("✅ Meilleure opportunité mondiale :")
        print(json.dumps(top, indent=4, default=lambda o: float(o)))
    else:
        print("❌ Aucune opportunité détectée.")
