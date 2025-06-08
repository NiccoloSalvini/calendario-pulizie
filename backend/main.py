# calendario-pulizie/backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Abilita CORS per consentire richieste dal frontend Netlify
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SMOOBU_TOKEN = os.getenv("SMOOBU_TOKEN")
BASE_URL = "https://login.smoobu.com/api"

@app.get("/prenotazioni")
def get_bookings():
    headers = {"API-Key": SMOOBU_TOKEN}
    response = requests.get(f"{BASE_URL}/bookings", headers=headers)

    # DEBUG LOG
    print("=== STATUS CODE ===", response.status_code)
    print("=== RESPONSE ===", response.text)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)
    return response.json()
