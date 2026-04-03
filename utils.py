def evaluate_signal_strength(signal):
    if signal["bias"] == "USD_BEARISH" and signal["category"] == "MODERATE":
        return "HIGH_CONFIDENCE"

    if signal["bias"] == "HIGH_VOLATILITY":
        return "AVOID"

    return "NORMAL"


def compute_performance(df):
    if df.empty or "pnl" not in df.columns:
        return {}

    trades = df[df["action"].notnull()]

    wins = trades[trades["pnl"] > 0]
    losses = trades[trades["pnl"] <= 0]

    return {
        "total_trades": len(trades),
        "win_rate": round(len(wins) / len(trades) * 100, 2) if len(trades) else 0,
        "avg_win": round(wins["pnl"].mean(), 2) if not wins.empty else 0,
        "avg_loss": round(losses["pnl"].mean(), 2) if not losses.empty else 0
    }


def suggest_trade(price, signal):
    if signal["action"] == "BUY":
        return {
            "entry": price,
            "sl": round(price - 0.0030, 5),
            "tp": round(price + 0.0050, 5)
        }

    if signal["action"] == "SELL":
        return {
            "entry": price,
            "sl": round(price + 0.0030, 5),
            "tp": round(price - 0.0050, 5)
        }

    return None
