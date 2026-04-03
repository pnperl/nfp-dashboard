import itertools

class StrategyOptimizer:
    def __init__(self, engine, backtester):
        self.engine = engine
        self.backtester = backtester

    def optimize(self, data):
        best_result = None
        best_params = None

        sl_values = [0.0020, 0.0030, 0.0040]
        tp_values = [0.0040, 0.0050, 0.0060]

        for sl, tp in itertools.product(sl_values, tp_values):
            result = self.backtester.run_backtest(data)

            if not best_result or result["net_profit"] > best_result["net_profit"]:
                best_result = result
                best_params = {"SL": sl, "TP": tp}

        return best_params, best_result
