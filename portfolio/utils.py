def get_risk_score(user_id):
    return 42  # example value

def get_var(user_id):
    return 1000.0  # example VaR

def buy_stock(user_id, symbol, quantity):
    print(f"Buying {quantity} shares of {symbol} for user {user_id}")
    return True

def sell_stock(user_id, symbol, quantity):
    print(f"Selling {quantity} shares of {symbol} for user {user_id}")
    return True
