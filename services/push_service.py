import datetime

import pymysql
from dbutils.pooled_db import PooledDB
import config as c


class push_service:

    def __init__(self):
        self.host = c.host
        self.user = c.user
        self.passwd = c.passwd
        self.port = c.port
        self.pool = self.connect()

    def connect(self):
        """
        创建mySql连接池
        :return:
        """
        max_connections = 15
        pool = PooledDB(pymysql,
                        max_connections,
                        host=self.host,
                        user=self.user,
                        passwd=self.passwd,
                        port=self.port,
                        db=c.database,
                        use_unicode=True)
        return pool

    def insert_market(self, market_data):
        """
        插入行情表
        :param market_data:
        :return:
        """
        db = self.pool.steady_connection()
        cur = db.cursor()
        sql = "INSERT IGNORE INTO market " \
              "(BUSI_DATE,STOCK_CODE,COMPANY,OCCUR_TIME,OPEN_PRICE,HIGH_PRICE,LOW_PRICE,LAST_PRICE,VOLUME) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) " \
              "AS NEW(BUSI_DATE,STOCK_CODE,COMPANY,OCCUR_TIME,OPEN_PRICE,HIGH_PRICE,LOW_PRICE,LAST_PRICE,VOLUME)" \
              "ON DUPLICATE KEY UPDATE " \
              "BUSI_DATE = NEW.BUSI_DATE, " \
              "COMPANY = NEW.COMPANY," \
              "OPEN_PRICE = NEW.OPEN_PRICE," \
              "HIGH_PRICE = NEW.HIGH_PRICE," \
              "LOW_PRICE = NEW.LOW_PRICE," \
              "LAST_PRICE = NEW.LAST_PRICE," \
              "VOLUME = NEW.VOLUME;"

        args = market_data
        try:
            cur.executemany(sql, args)
            db.commit()
        except Exception as e:
            db.rollback()
            print("SQL执行错误，原因: ", e)
        finally:
            cur.close()
            db.close()

    def insert_hist_market(self, hist_market_data):
        """
        插入历史行情表
        :param hist_market_data:
        :return:
        """
        db = self.pool.steady_connection()
        cur = db.cursor()
        sql = "INSERT IGNORE INTO hist_market " \
              "(BUSI_DATE,STOCK_CODE,OPEN_PRICE,CLOSE_PRICE,HIGH_PRICE,LOW_PRICE,VOLUME,TURNOVER) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s) " \
              "AS NEW(BUSI_DATE,STOCK_CODE,OPEN_PRICE,CLOSE_PRICE,HIGH_PRICE,LOW_PRICE,VOLUME,TURNOVER) " \
              "ON DUPLICATE KEY UPDATE " \
              "OPEN_PRICE = NEW.OPEN_PRICE," \
              "HIGH_PRICE = NEW.HIGH_PRICE," \
              "LOW_PRICE = NEW.LOW_PRICE," \
              "CLOSE_PRICE = NEW.CLOSE_PRICE," \
              "VOLUME = NEW.VOLUME," \
              "TURNOVER = NEW.TURNOVER;"
        args = hist_market_data
        try:
            cur.executemany(sql, args)
            db.commit()
        except Exception as e:
            db.rollback()
            print("SQL执行错误，原因: ", e)
        finally:
            cur.close()
            db.close()

    def insert_stocks(self, stock_data):
        """
        插入Stock表
        :param stock_data:
        :return:
        """
        db = self.pool.steady_connection()
        cur = db.cursor()
        sql = "INSERT IGNORE INTO stock " \
              "(STOCK_CODE,COMPANY,API_STOCK_CODE) " \
              "VALUES (%s,%s,%s) ;"
        args = stock_data
        try:
            cur.executemany(sql, args)
            db.commit()
        except Exception as e:
            db.rollback()
            print("SQL执行错误，原因: ", e)
        finally:
            cur.close()
            db.close()

    def insert_trade(self, trade):
        """
         插入trade表
        :param trade:
        :return:
        """
        db = self.pool.steady_connection()
        cur = db.cursor()
        sql = "INSERT IGNORE INTO trade " \
              "(STOCK_CODE,OCCUR_TIME,TRADE_SIGNAL,POSITION,MODEL_ID) " \
              "VALUES ('{}','{}','{}','{}','{}') " \
              "AS NEW(STOCK_CODE,OCCUR_TIME,TRADE_SIGNAL,POSITION,MODEL_ID) " \
              "ON DUPLICATE KEY UPDATE " \
              "TRADE_SIGNAL = NEW.TRADE_SIGNAL;" \
            .format(trade.stock_code, trade.occur_time, trade.trade_signal,
                    trade.position, trade.model_id)
        try:
            cur.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()
            print("SQL执行错误，原因: ", e)
        finally:
            cur.close()
            db.close()

    def insert_news(self, news):
        """
        插入news表
        :param news:
        :return:
        """
        db = self.pool.steady_connection()
        cur = db.cursor()
        sql = "INSERT IGNORE INTO news " \
              "(BUSI_DATE,TITLE,LINK) " \
              "VALUES (%s,%s,%s) " \
              "AS NEW(BUSI_DATE,TITLE,LINK)" \
              "ON DUPLICATE KEY UPDATE " \
              "LINK = NEW.LINK;"
        args = news
        try:
            cur.executemany(sql, args)
            db.commit()
        except Exception as e:
            db.rollback()
            print("SQL执行错误，原因: ", e)
        finally:
            cur.close()
            db.close()

    def insert_statistics(self, statistics):
        """
        插入stock_statistics表
        :param news:
        :return:
        """
        db = self.pool.steady_connection()
        cur = db.cursor()
        sql = "INSERT IGNORE INTO stock_statistics " \
              "(stock_code, " \
              "idex, market_cap, income, sales, book_per_sh, cash_per_sh, " \
              "dividend, dividend_percent, employees, optionable, shortable, recom, " \
              "PE, forward_PE, PEG, PS, PB, PC, " \
              "PFCF, quick_ratio, current_ratio, debt_per_eq, LT_debt_per_eq, sma20, " \
              "EPS_TTM,EPS_NEXT_Y, EPS_NEXT_Q, EPS_THIS_Y, EPS_NEXT_Y2, EPS_NEXT_5Y, " \
              "EPS_PAST_5Y, SALES_PAST_5Y,SALES_QQ, EPS_QQ, earnings, sma50, " \
              "insider_own, insider_trans, inst_own, inst_trans, ROA,ROE, " \
              "ROI, gross_margin, oper_margin, profit_margin, payout, sma200, " \
              "shares_outstand,shares_float, short_float, short_ratio, target_price, 52w_range, " \
              "52w_high, 52w_low,RSI14, rel_volume, avg_volume, volume, " \
              "perf_week, perf_month,perf_quarter, perf_half_Y,perf_year, perf_ytd, " \
              "beta, ATR, volatility, prev_close, price, chang) " \
              "VALUES (%s," \
              "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
              "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
              "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
              "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
              "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
              "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" \
              "AS NEW(stock_code, " \
              "idex, market_cap, income, sales, book_per_sh, cash_per_sh, " \
              "dividend, dividend_percent, employees, optionable, shortable, recom, " \
              "PE, forward_PE, PEG, PS, PB, PC, " \
              "PFCF, quick_ratio, current_ratio, debt_per_eq, LT_debt_per_eq, sma20, " \
              "EPS_TTM,EPS_NEXT_Y, EPS_NEXT_Q, EPS_THIS_Y, EPS_NEXT_Y2, EPS_NEXT_5Y, " \
              "EPS_PAST_5Y, SALES_PAST_5Y,SALES_QQ, EPS_QQ, earnings, sma50, " \
              "insider_own, insider_trans, inst_own, inst_trans, ROA,ROE, " \
              "ROI, gross_margin, oper_margin, profit_margin, payout, sma200, " \
              "shares_outstand,shares_float, short_float, short_ratio, target_price, 52w_range, " \
              "52w_high, 52w_low,RSI14, rel_volume, avg_volume, volume, " \
              "perf_week, perf_month,perf_quarter, perf_half_Y,perf_year, perf_ytd, " \
              "beta, ATR, volatility, prev_close, price, chang)" \
              "ON DUPLICATE KEY UPDATE " \
              "idex = NEW.idex, market_cap = NEW.market_cap, income = NEW.income, sales = NEW.sales,book_per_sh = NEW.book_per_sh, cash_per_sh = NEW.cash_per_sh, " \
              "dividend = NEW.dividend, dividend_percent = NEW.dividend_percent, employees = NEW.employees, optionable = NEW.optionable, shortable = NEW.shortable, recom = NEW.recom, " \
              "PE = NEW.PE, forward_PE = NEW.forward_PE, PEG = NEW.PEG, PS = NEW.PS, PB = NEW.PB, PC = NEW.PC, " \
              "PFCF = NEW.PFCF, quick_ratio = NEW.quick_ratio, current_ratio = NEW.current_ratio, debt_per_eq = NEW.debt_per_eq, LT_debt_per_eq = NEW.LT_debt_per_eq, sma20 = NEW.sma20," \
              "EPS_TTM = NEW.EPS_TTM,EPS_NEXT_Y = NEW.EPS_NEXT_Y, EPS_NEXT_Q = NEW.EPS_NEXT_Q, EPS_THIS_Y = NEW.EPS_THIS_Y, EPS_NEXT_Y2 = NEW.EPS_NEXT_Y2, EPS_NEXT_5Y = NEW.EPS_NEXT_5Y, " \
              "EPS_PAST_5Y = NEW.EPS_PAST_5Y, SALES_PAST_5Y = NEW.SALES_PAST_5Y,SALES_QQ = NEW.SALES_QQ, EPS_QQ = NEW.EPS_QQ, earnings = NEW.earnings, sma50 = NEW.sma50, " \
              "insider_own = NEW.insider_own, insider_trans = NEW.insider_trans, inst_own = NEW.inst_own, inst_trans = NEW.inst_trans,ROA = NEW.ROA, ROE = NEW.ROE, " \
              "ROI = NEW.ROI , gross_margin = NEW.gross_margin, oper_margin = NEW.oper_margin, profit_margin= NEW.profit_margin, payout = NEW.payout, sma200=NEW.sma200, " \
              "shares_outstand = NEW.shares_outstand,shares_float = NEW.shares_float, short_float = NEW.short_float, short_ratio = NEW.short_ratio, target_price = NEW.target_price, 52w_range = NEW.52w_range, " \
              "52w_high = NEW.52w_high, 52w_low = NEW.52w_low,RSI14 = NEW.RSI14, rel_volume = NEW.rel_volume, avg_volume = NEW.avg_volume, volume = NEW.volume, " \
              "perf_week = NEW.perf_week ,perf_month = NEW.perf_month,perf_quarter = NEW.perf_quarter, perf_half_Y = NEW.perf_half_Y,perf_year = NEW.perf_year, perf_ytd = NEW.perf_ytd, " \
              "beta = NEW.beta, ATR = NEW.ATR, volatility = NEW.volatility, prev_close = NEW.prev_close, price = NEW.price, chang = NEW.chang;"
        args = statistics
        try:
            cur.executemany(sql, args)
            db.commit()
        except Exception as e:
            db.rollback()
            print("SQL执行错误，原因: ", e)
        finally:
            cur.close()
            db.close()


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     stock_list = ['gb_jpm', 'gb_ibm', 'gb_msft','gb_aapl']
#     end_date = datetime.datetime.now() - datetime.timedelta(37)
#     start_date = end_date - datetime.timedelta(30)
#     for s in stock_list:
#         for d in range(0, 31):
#             d_date = start_date + datetime.timedelta(d)
#             sd = d_date.strftime("%Y%m%d")
#             data_list = ss.subscribe_stocks(s, sd)
#             push_service().insert_hist_market(data_list)



    # for s in stock_list:
    #     for d in date_list:
    #         data_list = ss.subscribe_stocks(s, d)
    #         push_service().insert_hist_market(data_list)
