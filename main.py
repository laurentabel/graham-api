from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

# PERMITIR WORDPRESS / ELEMENTOR
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"mensaje": "API funcionando"}

@app.get("/graham/{ticker}")
def graham(ticker: str):

    stock = yf.Ticker(ticker)
    info = stock.info

    price = info.get("currentPrice") or info.get("regularMarketPrice")
    eps = info.get("trailingEps")

    if price is None or eps is None:
        return {
            "ticker": ticker.upper(),
            "error": "No se pudo obtener precio o EPS"
        }

    g = 12
    y = 4.5

    valor_graham = eps * (8.5 + 2 * g) * 4.4 / y
    diferencial = ((valor_graham / price) - 1) * 100

    return {
        "ticker": ticker.upper(),
        "precio": round(price, 2),
        "valor_graham": round(valor_graham, 2),
        "diferencial_pct": round(diferencial, 2)
    }
