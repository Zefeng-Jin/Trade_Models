import copy
import datetime as dt
import time

import indicators_handler as handler
import push_service as db
import subscribe_service as untils


# noinspection DuplicatedCode
class MovingAverage:
    open_trade = []
    trade = []
    open_trade = []
    long_take_profit = []
    long_stop_loss = []
    long_entry_price = []
    short_take_profit = []
    short_stop_loss = []
    short_entry_price = []

    def __init__(self, stock_code, art_sl):
        """
        初始化参数
        :param stock_code: 证券代码
        :param art_sl: 风险承受能力   09·
        """
        # 输入股票代码
        self.stock_code = stock_code
        # 获取行情数据
        self.df = untils.subscribe(self.stock_code)
        # 振幅率
        self.art_sl = art_sl
        # 调度模型
        self.schedule()

    def trade_signal(self, pos):
        """
         计算交易信号
        :return:
        """
        stock = copy.deepcopy(self.df)
        stock['ATR'] = handler.atr(stock, 20)['ATR']
        stock = handler.sma(stock, 50, 200)
        signal = ''
        if pos == '':
            if stock['ema_fast'][-2] < stock['ema_slow'][-2] \
                    and stock['ema_fast'][-1] >= stock['ema_slow'][-1] \
                    and len(self.open_trade) == 0:
                self.trade[stock.index[-1]] = {'date_of_trade': stock.index[-1],
                                               'entry_price': stock['Close'][-1],
                                               'signal': 'Buy',
                                               'result': 0,
                                               'TP': stock['Close'][-1] + stock['ATR'][-1] * self.art_sl,
                                               'SL': stock['Close'][-1] - stock['ATR'][-1] * self.art_sl}
                self.open_trade.append(stock.index[-1])
                self.long_take_profit.append(self.trade[stock.index[-1]]['TP'])
                self.long_stop_loss.append(self.trade[stock.index[-1]]['SL'])
                self.long_entry_price.append(self.trade[stock.index[-1]]['entry_price'])
                signal = "Buy"
            elif stock['ema_fast'][-2] > stock['ema_slow'][-2] \
                    and stock['ema_fast'][-1] <= stock['ema_slow'][-1] \
                    and len(self.open_trade) == 0:
                self.trade[stock.index[-1]] = {'date_of_trade': stock.index[-1],
                                               'entry_price': stock['Close'][-1],
                                               'signal': 'Buy',
                                               'result': 0,
                                               'TP': stock['Close'][-1] - stock['ATR'][-1] * self.art_sl,
                                               'SL': stock['Close'][-1] + stock['ATR'][-1] * self.art_sl}
                self.open_trade.append(stock.index[-1])
                self.short_take_profit.append(self.trade[stock.index[-1]]['TP'])
                self.short_stop_loss.append(self.trade[stock.index[-1]]['SL'])
                self.short_entry_price.append(self.trade[stock.index[-1]]['entry_price'])
                signal = "Sell"
        elif pos == "long":
            if any(y <= stock['Close'][-1] for y in self.long_take_profit):
                for j in self.open_trade:
                    if self.trade[j].get('result', {}) == 0 and self.trade[j].get('signal', {}) == 'Buy':
                        if stock['Close'][-1] >= self.trade[j]['TP']:
                            self.trade[j].update({'result': (self.trade[j]['TP'] - self.trade[j]['entry_price'])})
                            self.open_trade.remove(j)
                            self.long_take_profit.remove(self.trade[j][j]['TP'])
                            self.long_stop_loss.remove(self.trade[j]['SL'])
                            signal = "Close"
            elif any(y >= self.stock['Close'][-1] for y in self.long_stop_loss):
                for j in self.open_trade:
                    if self.trade[j].get('result', {}) == 0 and self.trade[j].get('signal', {}) == 'Buy':
                        if stock['Close'][-1] <= self.trade[j]['SL']:
                            self.trade[j].update(
                                {'result': (self.trade[j]['SL'] - self.trade[j]['entry_price'])})
                            self.open_trade.remove(j)
                            self.long_take_profit.remove(self.trade[j]['TP'])
                            self.long_stop_loss.remove(self.trade[j]['SL'])
                            signal = "Close_Sell"
        elif pos == "short":
            if any(y >= stock['Close'][-1] for y in self.short_take_profit):
                for j in self.open_trade:
                    if self.trade[j].get('result', {}) == 0 and self.trade[j].get('signal', {}) == 'Sell':
                        if stock['Close'][-1] <= self.trade[j]['TP']:
                            self.trade[j].update(
                                {'result': (self.trade[j]['entry_price'] - self.trade[j]['TP'])})
                            self.open_trade.remove(j)
                            self.short_take_profit.remove(self.trade[j]['TP'])
                            self.short_stop_loss.remove(self.trade[j]['SL'])
                            signal = "Close"
            elif any(y <= stock['Close'][-1] for y in self.short_stop_loss):
                for j in self.open_trade:
                    if self.trade[j].get('result', {}) == 0 and self.trade[self.stock_code][j].get('signal',
                                                                                                   {}) == 'Sell':
                        if stock['Close'][-1] >= self.trade[j]['SL']:
                            self.trade[j].update(
                                {'result': (self.trade[j]['entry_price'] - self.trade[j]['SL'])})
                            self.open_trade.remove(j)
                            self.short_take_profit.remove(self.trade[j]['TP'])
                            self.short_stop_loss.remove(self.trade[j]['SL'])
                            signal = "Close_Buy"
        return signal

    def run(self):
        """
        运行程序
        :return:
        """
        try:
            api = untils.trade_api()
            open_pos = api.list_positions()
            pos = ''
            if len(open_pos) > 0:
                for i in range(len(open_pos)):
                    if open_pos[i].symbol == self.stock_code:
                        open_pos_code = open_pos[i]
                        pos = open_pos_code.side
            signal = self.trade_signal(pos)
            if signal == "Buy":
                api.submit_order(symbol=self.stock_code, qty=10, side='buy', time_in_force='gtc', type='stop_limit',
                                 stop_price=self.df['Close'][-1] * 0.99,
                                 limit_price=self.df['Close'][-1] * 1.02)
                print("New long position initiated for {}, at price {} ".format(self.stock_code, self.df['Close'][-1]))
            elif signal == "Sell":
                api.submit_order(symbol=self.stock_code, qty=10, side='sell', time_in_force='gtc', type='stop_limit',
                                 stop_price=self.df['Close'][-1] * 1.01,
                                 limit_price=self.df['Close'][-1] * 0.98)
                print("New short position initiated for {}, at price {} ".format(self.stock_code, self.df['Close'][-1]))
            elif signal == "Close":
                api.close_position(self.stock_code)
                print("All positions closed for {}， at price {} ".format(self.stock_code, self.df['Close'][-1]))
            elif signal == "Close_Buy":
                api.close_position(self.stock_code)
                print(
                    "Existing Short position closed for  {}， at price {} ".format(self.stock_code,
                                                                                  self.df['Close'][-1]))
                api.submit_order(symbol=self.stock_code, qty=10, side='buy', time_in_force='gtc', type='stop_limit',
                                 stop_price=self.df['Close'][-1] * 0.99,
                                 limit_price=self.df['Close'][-1] * 1.02)
                print("New long position initiated for  {}， at price {} ".format(self.stock_code, self.df['Close'][-1]))
            elif signal == "Close_Sell":
                api.close_position(self.stock_code)
                print(
                    "Existing long position closed for  {}， at price {} ".format(self.stock_code, self.df['Close'][-1]))
                api.submit_order(symbol=self.stock_code, qty=10, side='sell', time_in_force='gtc', type='stop_limit',
                                 stop_price=self.df['Close'][-1] * 1.01,
                                 limit_price=self.df['Close'][-1] * 0.98)
                print(
                    "New short position initiated for  {}， at price {} ".format(self.stock_code, self.df['Close'][-1]))
        except:
            print("error encountered....skipping this iteration")

    def schedule(self):
        """
        调度程序
        :return:
        """
        timeout = time.time() + 60 * 60 * 5  # 60 seconds times 60 time 5 meaning the script will run for 5 hr
        while time.time() <= timeout:
            try:
                print("pass through at ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                self.run()
                self.push()
                time.sleep(300)  # 5 minute interval between each new execution
            except KeyboardInterrupt:
                print('\n\nKeyboard exception received. Exiting.')
                exit()

    def push(self):
        """
        推送数据库
        :return:
        """
        for i in range(len(self.df)):
            market = []
            date = dt.datetime.now().date().strftime("%Y%m%d")
            market.append(date)
            market.append(self.stock_code)
            market.append(self.df.index[i])
            for j in range(len(self.df.iloc[i])):
                market.append(self.df.iloc[i, j])
            db.dbConn().insert_market(market)
