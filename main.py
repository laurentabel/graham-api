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
@app.get("/umb/{ticker}")
def umb_score(ticker: str):

    stock = yf.Ticker(ticker)
    info = stock.info

    price = info.get("currentPrice") or info.get("regularMarketPrice")
    high_52 = info.get("fiftyTwoWeekHigh")
    low_52 = info.get("fiftyTwoWeekLow")

    if price is None or high_52 is None or low_52 is None:
        return {
            "ticker": ticker.upper(),
            "error": "No se pudieron obtener datos"
        }

    upside_pct = ((high_52 / price) - 1) * 100

    downside_pct = ((low_52 / price) - 1) * 100

    risk_pct = abs(downside_pct)

    if risk_pct == 0:
        gain_loss = 0
    else:
        gain_loss = upside_pct / risk_pct

    price_to_high_52 = price / high_52

    valid_momentum = price_to_high_52 >= 0.70

    # SCORE

    if gain_loss >= 3:
        score_label = "Excelente beneficio/riesgo"
        score_color = "green"

    elif gain_loss >= 2:
        score_label = "Muy buen beneficio/riesgo"
        score_color = "green"

    elif gain_loss >= 1:
        score_label = "Beneficio mayor que riesgo"
        score_color = "yellow"

    elif gain_loss >= 0.7:
        score_label = "Riesgo ligeramente mayor"
        score_color = "orange"

    else:
        score_label = "Riesgo mayor que beneficio"
        score_color = "red"

    return {

        "ticker": ticker.upper(),

        "precio": round(price, 2),

        "high_52w": round(high_52, 2),

        "low_52w": round(low_52, 2),

        "upside_pct": round(upside_pct, 2),

        "downside_pct": round(downside_pct, 2),

        "gain_loss": round(gain_loss, 2),

        "price_to_high_52": round(price_to_high_52, 2),

        "valid_momentum": valid_momentum,

        "score_label": score_label,

        "score_color": score_color
    }
