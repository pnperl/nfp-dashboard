def interpret_nfp(self, signal):
    if signal["category"] == "VERY_STRONG":
        return "USD likely strong, rate cuts delayed → EURUSD bearish"

    if signal["category"] == "MODERATE":
        return "Goldilocks zone → USD weakness → EURUSD bullish"

    if signal["category"] == "WEAK":
        return "Economic slowdown → USD weak → EURUSD bullish"

    if signal["category"] == "VERY_WEAK":
        return "Recession risk → high volatility, avoid trading"

    return "No clear edge"
