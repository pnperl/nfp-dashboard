class NFPEngine:
    def calculate_surprise(self, actual, forecast):
        return actual - forecast

    def classify_nfp(self, surprise):
        if surprise > 100000:
            return "VERY_STRONG"
        elif 30000 <= surprise <= 100000:
            return "MODERATE"
        elif -30000 <= surprise < 30000:
            return "NEUTRAL"
        elif -100000 <= surprise < -30000:
            return "WEAK"
        else:
            return "VERY_WEAK"

    def usd_bias(self, category):
        mapping = {
            "VERY_STRONG": "USD_BULLISH",
            "MODERATE": "USD_BEARISH",
            "NEUTRAL": "NO_TRADE",
            "WEAK": "USD_BEARISH",
            "VERY_WEAK": "HIGH_VOLATILITY"
        }
        return mapping.get(category, "NO_TRADE")

    def generate_signal(self, actual, forecast):
        surprise = self.calculate_surprise(actual, forecast)
        category = self.classify_nfp(surprise)
        bias = self.usd_bias(category)

        signal = {
            "surprise": surprise,
            "category": category,
            "bias": bias,
            "pair": None,
            "action": None
        }

        if bias == "USD_BEARISH":
            signal["pair"] = "EURUSD"
            signal["action"] = "BUY"
        elif bias == "USD_BULLISH":
            signal["pair"] = "EURUSD"
            signal["action"] = "SELL"

        return signal
