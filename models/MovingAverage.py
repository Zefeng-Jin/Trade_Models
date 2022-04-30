import concurrent.futures as cf
import copy
import time

import indicators_handler as handler
import model_constant as mc
from services import push_service as ps, query_service as qs
from table_structure.trade import Trade


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
    pos = ''

    def __init__(self, stock_list, art_sl):
        """
        初始化参数
        :param stock_code: 证券代码
        :param art_sl: 风险承受能力   09·
        """
        # 输入股票代码
        self.stock_list = stock_list
        # 振幅率
        self.art_sl = art_sl
        # 调度模型
        self.schedule()

    def trade_signal(self, pos, df):
        """
        计算交易信号
        :param pos: position(long/short)
        :return:
        """
        """
         计算交易信号
        :return:
        """
        stock = copy.deepcopy(df)
        stock['ATR'] = handler.atr(stock, 20)['ATR']
        stock = handler.sma(stock, 50, 200)
        signal = ''
        if pos == '':
            if stock['ema_fast'][-2] < stock['ema_slow'][-2] \
                    and stock['ema_fast'][-1] >= stock['ema_slow'][-1] \
                    and len(self.open_trade) == 0:
                self.trade[stock.index[-1]] = {'date_of_trade': stock.index[-1],
                                               'entry_price': stock['last_price'][-1],
                                               'signal': 'Buy',
                                               'result': 0,
                                               'TP': stock['last_price'][-1] + stock['ATR'][-1] * self.art_sl,
                                               'SL': stock['last_price'][-1] - stock['ATR'][-1] * self.art_sl}
                self.open_trade.append(stock.index[-1])
                self.long_take_profit.append(self.trade[stock.index[-1]]['TP'])
                self.long_stop_loss.append(self.trade[stock.index[-1]]['SL'])
                self.long_entry_price.append(self.trade[stock.index[-1]]['entry_price'])
                signal = "Buy"
            elif stock['ema_fast'][-2] > stock['ema_slow'][-2] \
                    and stock['ema_fast'][-1] <= stock['ema_slow'][-1] \
                    and len(self.open_trade) == 0:
                self.trade[stock.index[-1]] = {'date_of_trade': stock.index[-1],
                                               'entry_price': stock['last_price'][-1],
                                               'signal': 'Buy',
                                               'result': 0,
                                               'TP': stock['last_price'][-1] - stock['ATR'][-1] * self.art_sl,
                                               'SL': stock['last_price'][-1] + stock['ATR'][-1] * self.art_sl}
                self.open_trade.append(stock.index[-1])
                self.short_take_profit.append(self.trade[stock.index[-1]]['TP'])
                self.short_stop_loss.append(self.trade[stock.index[-1]]['SL'])
                self.short_entry_price.append(self.trade[stock.index[-1]]['entry_price'])
                signal = "Sell"
        elif pos == "long":
            if any(y <= stock['last_price'][-1] for y in self.long_take_profit):
                for j in self.open_trade:
                    if self.trade[j].get('result', {}) == 0 and self.trade[j].get('signal', {}) == 'Buy':
                        if stock['last_price'][-1] >= self.trade[j]['TP']:
                            self.trade[j].update({'result': (self.trade[j]['TP'] - self.trade[j]['entry_price'])})
                            self.open_trade.remove(j)
                            self.long_take_profit.remove(self.trade[j][j]['TP'])
                            self.long_stop_loss.remove(self.trade[j]['SL'])
                            signal = "Close"
            elif any(y >= self.stock['last_price'][-1] for y in self.long_stop_loss):
                for j in self.open_trade:
                    if self.trade[j].get('result', {}) == 0 and self.trade[j].get('signal', {}) == 'Buy':
                        if stock['last_price'][-1] <= self.trade[j]['SL']:
                            self.trade[j].update(
                                {'result': (self.trade[j]['SL'] - self.trade[j]['entry_price'])})
                            self.open_trade.remove(j)
                            self.long_take_profit.remove(self.trade[j]['TP'])
                            self.long_stop_loss.remove(self.trade[j]['SL'])
                            signal = "Close_Sell"
        elif pos == "short":
            if any(y >= stock['last_price'][-1] for y in self.short_take_profit):
                for j in self.open_trade:
                    if self.trade[j].get('result', {}) == 0 and self.trade[j].get('signal', {}) == 'Sell':
                        if stock['last_price'][-1] <= self.trade[j]['TP']:
                            self.trade[j].update(
                                {'result': (self.trade[j]['entry_price'] - self.trade[j]['TP'])})
                            self.open_trade.remove(j)
                            self.short_take_profit.remove(self.trade[j]['TP'])
                            self.short_stop_loss.remove(self.trade[j]['SL'])
                            signal = "Close"
            elif any(y <= stock['last_price'][-1] for y in self.short_stop_loss):
                for j in self.open_trade:
                    if self.trade[j].get('result', {}) == 0 and self.trade[self.stock_code][j].get('signal',
                                                                                                   {}) == 'Sell':
                        if stock['last_price'][-1] >= self.trade[j]['SL']:
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
        executor = cf.ThreadPoolExecutor(max_workers=5)
        wait_for = [executor.submit(self.insert_trade, stock) for stock in self.stock_list]
        for f in cf.as_completed(wait_for):
            print(f.result())

    def insert_trade(self, s):
        """
        插入trade数据
        :param s:
        :return:
        """
        # 获取行情数据
        message = 'success'
        try:
            df = qs.query_service().get_hist_market(s)
            signal = self.trade_signal(self.pos, df)
            if signal == "Buy":
                self.pos = 'long'
                trade = Trade(df[-1]['stock_code'], df[-1]['occur_time'], signal, self.pos, mc.MovingAverage)
                ps.push_service().insert_trade(trade)
            elif signal == "Sell":
                self.pos = 'short'
                trade = Trade(df[-1]['stock_code'], df[-1]['occur_time'], signal, self.pos, mc.MovingAverage)
                ps.push_service().insert_trade(trade)
            elif signal == "Close" or signal == "Close_Buy" or signal == "Close_Sell":
                trade = Trade(df[-1]['stock_code'], df[-1]['occur_time'], signal, self.pos, mc.MovingAverage)
                ps.push_service().insert_trade(trade)
            self.pos = ''
            return message
        except:
            return message

    def schedule(self):
        """
        调度程序
        :return:
        """
        while True:
            try:
                self.run()
                time.sleep(60)  # 1 minute interval between each new execution
            except KeyboardInterrupt:
                print('\n\nKeyboard exception received. Exiting.')
                exit()


if __name__ == '__main__':
    stock_list = ['gb_jpm', 'gb_aapl', 'gb_msft']
    MovingAverage(stock_list, 0.1).schedule()
