import pandas as pd

class NFPBacktester:
    def __init__(self, engine, initial_capital=10000):
        self.engine = engine
        self.initial_capital = initial_capital
        self.results = []

    def run_backtest(self, data):
        equity = self.initial_capital
        peak = equity
        max_drawdown = 0

        for _, row in data.iterrows():

            signal = self.engine.generate_signal(row['actual'], row['forecast'])

            if signal["action"] is None:
                continue

            entry = row['price_entry']
            exit_price = row['price_exit']

            # realism
            spread = 0.0002
            slippage = 0.0001

            entry += spread
            exit_price -= slippage

            if signal["action"] == "BUY":
                pnl = (exit_price - entry) * 100000
            else:
                pnl = (entry - exit_price) * 100000

            equity += pnl

            peak = max(peak, equity)
            drawdown = peak - equity
            max_drawdown = max(max_drawdown, drawdown)

            self.results.append({
                "date": row['date'],
                "action": signal["action"],
                "entry": entry,
                "exit": exit_price,
                "pnl": pnl,
                "equity": equity
            })

        return self._metrics(equity, max_drawdown)

    def _metrics(self, final_equity, max_dd):
        df = pd.DataFrame(self.results)

        if df.empty:
            return {"error": "No trades generated"}

        wins = df[df['pnl'] > 0]
        losses = df[df['pnl'] <= 0]

        return {
            "total_trades": len(df),
            "win_rate": round(len(wins) / len(df) * 100, 2),
            "net_profit": round(final_equity - self.initial_capital, 2),
            "max_drawdown": round(max_dd, 2),
            "avg_win": round(wins['pnl'].mean(), 2) if not wins.empty else 0,
            "avg_loss": round(losses['pnl'].mean(), 2) if not losses.empty else 0,
            "results_df": df
        }
