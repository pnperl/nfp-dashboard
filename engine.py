class NFPEngine:

    # ---------------- CORE CALCULATION ----------------
    def calculate_surprise(self, actual, forecast):
        try:
            return float(actual) - float(forecast)
        except:
            return 0

    # ---------------- CLASSIFICATION ----------------
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

    # ---------------- USD BIAS ----------------
    def usd_bias(self, category):
        mapping = {
            "VERY_STRONG": "USD_BULLISH",
            "MODERATE": "USD_BEARISH",   # Goldilocks → rate cut expectations
            "NEUTRAL": "NO_TRADE",
            "WEAK": "USD_BEARISH",
            "VERY_WEAK": "HIGH_VOLATILITY"
        }
        return mapping.get(category, "NO_TRADE")

    # ---------------- SIGNAL GENERATION ----------------
    def generate_signal(self, actual, forecast):
        surprise = self.calculate_surprise(actual, forecast)
        category = self.classify_nfp(surprise)
        bias = self.usd_bias(category)

        signal = {
            "actual": actual,
            "forecast": forecast,
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

    # ---------------- INTERPRETATION ----------------
    def interpret_nfp(self, signal):
        category = signal.get("category")

        if category == "VERY_STRONG":
            return "Strong labor market → Inflation risk → Fed stays hawkish → USD strengthens → EURUSD likely bearish"

        elif category == "MODERATE":
            return "Balanced growth (Goldilocks) → Supports rate cuts → USD weakens → EURUSD bullish"

        elif category == "WEAK":
            return "Economic slowdown → Fed may cut rates → USD weakens → EURUSD bullish"

        elif category == "VERY_WEAK":
            return "Recession risk → Extreme volatility → Avoid trading"

        else:
            return "No clear macro edge"

    # ---------------- SIGNAL STRENGTH ----------------
    def evaluate_strength(self, signal):
        category = signal.get("category")
        bias = signal.get("bias")

        if category == "MODERATE" and bias == "USD_BEARISH":
            return "HIGH_CONFIDENCE"

        if category == "VERY_WEAK":
            return "AVOID"

        if category == "VERY_STRONG":
            return "STRONG_TREND"

        return "NORMAL"

    # ---------------- TRADE SETUP ----------------
    def suggest_trade(self, price, signal):
        if signal["action"] == "BUY":
            return {
                "entry": round(price, 5),
                "sl": round(price - 0.0030, 5),   # 30 pips
                "tp": round(price + 0.0050, 5),   # 50 pips
                "rr": round(0.0050 / 0.0030, 2)
            }

        elif signal["action"] == "SELL":
            return {
                "entry": round(price, 5),
                "sl": round(price + 0.0030, 5),
                "tp": round(price - 0.0050, 5),
                "rr": round(0.0050 / 0.0030, 2)
            }

        return None

    # ---------------- SUMMARY (FOR DASHBOARD) ----------------
    def summarize(self, signal, price=None):
        summary = {
            "Signal": signal["action"],
            "Pair": signal["pair"],
            "Category": signal["category"],
            "Bias": signal["bias"],
            "Surprise": signal["surprise"]
        }

        if price and signal["action"]:
            trade = self.suggest_trade(price, signal)
            summary.update(trade)

        return summary
