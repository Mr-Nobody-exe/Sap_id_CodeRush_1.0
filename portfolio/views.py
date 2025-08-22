from django.shortcuts import render

def portfolio_home(request):
    return render(request, 'portfolio/userProfile.html')


import requests
import pandas as pd
import numpy as np
from django.http import JsonResponse
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#Alpha Vantage API key
#https://www.alphavantage.co/

STOCK_API_KEY = "W4SMTYWRM655US2R"

#News API key
#https://newsapi.org/
NEWS_API_KEY = "cb30ab4d77a0429180cf6a103100f615"

analyzer = SentimentIntensityAnalyzer()


def get_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={STOCK_API_KEY}"
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

def calculate_volatility(returns):
    returns = returns.dropna()
    volatility = np.std(returns) * np.sqrt(252)  # Annualized volatility
    return float(volatility)

def get_sentiment(symbol):
    url = f"https://newsapi.org/v2/everything?q={symbol}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    r = requests.get(url)
    data = r.json()

    if "articles" not in data:
        return None

    articles = data["articles"][:5]  # Get the latest 5 articles
    sentiments = []


    for art in articles:
        headline = art["title"]
        score = analyzer.polarity_scores(headline)["compound"]
        sentiments.append(score)


    if sentiments:
        avg_sentiment = np.mean(sentiments)
    else:
        avg_sentiment = 0.0
    
    return float(avg_sentiment),[art["title"] for art in articles[:5]]


def suggest_action(var, cvar, volatility, sentiment):
    """
    Simple rule-based decision engine.
    Uses VaR, CVaR, Volatility, and Sentiment to suggest an action.
    """

    # Normalize risk (combine volatility + downside risk)
    risk_score = abs(var) + abs(cvar) + volatility  

    # Convert risk_score to percentage (just a scaling)
    risk_percent = min(risk_score * 100, 100)  

    # --- Decision Logic ---
    if sentiment > 0.2 and risk_percent < 30:
        action = "Buy"
        explanation = "Positive news sentiment and relatively low risk make this stock favorable."
    elif -0.2 <= sentiment <= 0.2 or 30 <= risk_percent <= 60:
        action = "Hold"
        explanation = "Neutral sentiment or moderate risk suggests waiting for clearer signals."
    else:
        action = "Sell"
        explanation = "Negative sentiment or high downside risk indicates caution."

    return {
        "Action": action,
        "Explanation": explanation,
        "Risk (%)": round(risk_percent, 2)
    }
    

def risk_metrics(request, symbol):
    df = get_stock_data(symbol)
    if df is None:
        return JsonResponse({"error": "Invalid symbol or API limit reached"}, status=400)

    df["return"] = df["close"].pct_change()
    var, cvar = calculate_var_cvar(df["return"])
    volatility = calculate_volatility(df["return"])
    sentiment, headlines = get_sentiment(symbol)
    decision = suggest_action(var, cvar, volatility, sentiment)


    return JsonResponse({
        "symbol": symbol,
        "VaR_95": var,
        "CVaR_95": cvar,
        "Volatility": volatility,
        "Sentiment": sentiment,
        "Headlines": headlines,
        "Suggested_Action": decision["Action"],
        "Explanation": decision["Explanation"],
        "Risk_Percent": decision["Risk (%)"]
    })

    


