def evaluate_signal_strength(signal):
    if signal["bias"] == "USD_BEARISH" and signal["category"] == "MODERATE":
        return "HIGH_CONFIDENCE"
    if signal["bias"] == "HIGH_VOLATILITY":
        return "AVOID"
    return "NORMAL"
