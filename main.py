from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "API funcionando"}

@app.get("/graham/{ticker}")
def graham(ticker: str):

    stock = yf.Ticker(ticker)
    info = stock.info

    price = info.get("currentPrice")
    eps = info.get("trailingEps")

    if not price or not eps:
        return {"error": "Datos insuficientes"}

    g = 12
    y = 4.5

    valor = eps * (8.5 + 2 * g) * 4.4 / y

    upside = ((valor / price) - 1) * 100

    return {
        "ticker": ticker.upper(),
        "precio": round(price,2),
        "valor_graham": round(valor,2),
        "diferencial_pct": round(upside,2)
    }
