import requests
import pandas as pd
import numpy as np
from django.http import JsonResponse

#Alpha Vantage API key
#https://www.alphavantage.co/

API_KEY = "W4SMTYWRM655US2R"   

def get_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={API_KEY}"
    r = requests.get(url)
    data = r.json()

    if "Time Series (Daily)" not in data:
        return None

    ts = data["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(ts, orient="index", dtype=float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df.rename(columns={"4. close": "close"}, inplace=True)
    return df

def calculate_var_cvar(returns, confidence=0.95):
    returns = returns.dropna()
    var = np.percentile(returns, (1 - confidence) * 100)
    cvar = returns[returns <= var].mean()
    return float(var), float(cvar)

def risk_metrics(request, symbol):
    df = get_stock_data(symbol)
    if df is None:
        return JsonResponse({"error": "Invalid symbol or API limit reached"}, status=400)

    df["return"] = df["close"].pct_change()
    var, cvar = calculate_var_cvar(df["return"])
    return JsonResponse({
        "symbol": symbol,
        "VaR_95": var,
        "CVaR_95": cvar,
        "Risk_Percent": Risk_Percent,
    })
