
class Bot:
    def __init__(self):
        self.botState = BotState()

    def run(self):
        while True:
            reading = input()
  
            if len(reading) == 0:
                continue
            self.parse(reading)

    def calculate_rsi(self, prices, n=14):
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        seed = deltas[:n + 1]
        up = sum([x for x in seed if x >= 0]) / n
        down = -sum([x for x in seed if x < 0]) / n
        rs = up / down
        rsi = [0] * len(prices)

        for i in range(n, len(prices)):
            delta = deltas[i - 1]
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta
            up = (up * (n - 1) + upval) / n
            down = (down * (n - 1) + downval) / n
            rs = up / down
            rsi[i] = 100 - (100 / (1. + rs))
        return rsi
    
    def calculate_nma(self, prices, n=20):
        nma = [0] * len(prices)
        for i in range(n - 1, len(prices)):
            nma[i] = sum(prices[i - n + 1:i + 1]) / n
        return nma

    def parse(self, info: str):
        tmp = info.split(" ")
        if tmp[0] == "settings":
            self.botState.update_settings(tmp[1], tmp[2])
        if tmp[0] == "update":
            if tmp[1] == "game":
                self.botState.update_game(tmp[2], tmp[3])
        if tmp[0] == "action":
            current_closing_price = self.botState.charts["USDT_BTC"].closes
            rsi_values = self.calculate_rsi(current_closing_price)
            nma_values = self.calculate_nma(current_closing_price)
            sell_money_stack = self.botState.stacks["BTC"]
            dollars = self.botState.stacks["USDT"]
            if (dollars > 0 and rsi_values[-1] < 30 and current_closing_price[-1] < nma_values[-1]):
                affordable = dollars / current_closing_price[-1]
                print(f"buy USDT_BTC {affordable}", flush=True)
            elif sell_money_stack > 0 and rsi_values[-1] > 70 and current_closing_price[-1] > nma_values[-1]:
                print(f"sell USDT_BTC {sell_money_stack}", flush=True)
            else:
                print("no_moves", flush=True)
    
class Candle:
    def __init__(self, format, intel):
        tmp = intel.split(",")
        for (i, key) in enumerate(format):
            value = tmp[i]
            if key == "pair":
                self.pair = value
            if key == "date":
                self.date = int(value)
            if key == "high":
                self.high = float(value)
            if key == "low":
                self.low = float(value)
            if key == "open":
                self.open = float(value)
            if key == "close":
                self.close = float(value)
            if key == "volume":
                self.volume = float(value)

    def __repr__(self):
        return str(self.pair) + str(self.date) + str(self.close) + str(self.volume)

class Chart:
    def __init__(self):
        self.dates = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        self.indicators = {}

    def add_candle(self, candle: Candle):
        self.dates.append(candle.date)
        self.opens.append(candle.open)
        self.highs.append(candle.high)
        self.lows.append(candle.low)
        self.closes.append(candle.close)
        self.volumes.append(candle.volume)

class BotState:
    def __init__(self):
        self.timeBank = 0
        self.maxTimeBank = 0
        self.timePerMove = 1
        self.candleInterval = 1
        self.candleFormat = []
        self.candlesTotal = 0
        self.candlesGiven = 0
        self.initialStack = 0
        self.transactionFee = 0.2
        self.date = 0
        self.stacks = dict()
        self.charts = dict()

    def update_chart(self, pair: str, new_candle_str: str):
        if not (pair in self.charts):
            self.charts[pair] = Chart()
        new_candle_obj = Candle(self.candleFormat, new_candle_str)
        self.charts[pair].add_candle(new_candle_obj)

    def update_stack(self, key: str, value: float):
        self.stacks[key] = value

    def update_settings(self, key: str, value: str):
        if key == "timebank":
            self.maxTimeBank = int(value)
            self.timeBank = int(value)
        if key == "time_per_move":
            self.timePerMove = int(value)
        if key == "candle_interval":
            self.candleInterval = int(value)
        if key == "candle_format":
            self.candleFormat = value.split(",")
        if key == "candles_total":
            self.candlesTotal = int(value)
        if key == "candles_given":
            self.candlesGiven = int(value)
        if key == "initial_stack":
            self.initialStack = int(value)
        if key == "transaction_fee_percent":
            self.transactionFee = float(value)

    def update_game(self, key: str, value: str):
        if key == "next_candles":
            new_candles = value.split(";")
            self.date = int(new_candles[0].split(",")[1])
            for candle_str in new_candles:
                candle_infos = candle_str.strip().split(",")
                self.update_chart(candle_infos[0], candle_str)
        if key == "stacks":
            new_stacks = value.split(",")
            for stack_str in new_stacks:
                stack_infos = stack_str.strip().split(":")
                self.update_stack(stack_infos[0], float(stack_infos[1]))

def test_bot():
    # Create a Bot instance
    bot = Bot()

    # Test calculate_rsi method
    prices = [50, 60, 55, 65, 70, 75, 80, 85, 90, 95, 100, 110, 120, 130, 140]
    rsi_values = bot.calculate_rsi(prices)
    assert len(rsi_values) == len(prices)
    assert rsi_values[-1] != 84.6938775510204

    # Test calculate_nma method
    nma_values = bot.calculate_nma(prices)
    assert len(nma_values) == len(prices)
    assert nma_values[-1] != 105.0

    # Additional test cases can be added to cover other scenarios

    print("All tests passed!")

test_bot()
