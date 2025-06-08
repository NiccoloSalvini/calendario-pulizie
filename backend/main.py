from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from datetime import datetime # <-- Importa datetime

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SMOOBU_TOKEN = os.getenv("SMOOBU_TOKEN")
if not SMOOBU_TOKEN:
    raise RuntimeError(
        "ERRORE: La variabile d'ambiente SMOOBU_TOKEN non è impostata. "
        "Assicurati di aver creato un file .env o di averla configurata correttamente."
    )
# Assicurati di usare questo URL base per le API
BASE_URL = "https://login.smoobu.com/api"


# niccolosalvini/calendario-pulizie/calendario-pulizie-e8dd90669023667c20a558ed494bc9e75c469092/backend/main.py

@app.get("/prenotazioni")
def get_bookings():
    token_letto = os.getenv("SMOOBU_TOKEN")
    headers = {"API-Key": token_letto}
    url = f"{BASE_URL}/reservations"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Errore di comunicazione con l'API di Smoobu: {e}")

    data = response.json()
    
    prenotazioni_processate = []
    for p in data.get("bookings", []):
        try:
            arrivo = datetime.fromisoformat(p.get("arrival"))
            partenza = datetime.fromisoformat(p.get("departure"))
            notti = (partenza - arrivo).days
        except (TypeError, ValueError):
            notti = "N/D"

        # --- QUESTA È LA PARTE CORRETTA ---
        adulti = p.get("adults") or 0
        bambini = p.get("children") or 0
        persone = adulti + bambini
        # -----------------------------------

        prenotazione_info = {
            "ospite": p.get("guest-name", "Ospite non specificato"),
            "notti": notti,
            "persone": persone,
            "data_arrivo": p.get("arrival"),
            "data_partenza": p.get("departure"),
        }
        prenotazioni_processate.append(prenotazione_info)

    return prenotazioni_processate