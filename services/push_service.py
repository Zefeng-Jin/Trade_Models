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

    def insert_stocks(self, stock_data):
        """
        插入Stock表
        :param stock_data:
        :return:
        """
        db = self.pool.steady_connection()
        cur = db.cursor()
        sql = "INSERT IGNORE INTO stock " \
              "(STOCK_CODE,COMPANY) " \
              "VALUES (%s,%s) ;"
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
              "VALUES (%s,%s,%s,%s,%s) ;".format(trade.stock_code, trade.occur_time, trade.trade_signal,
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

    #
    # def insert_profit_loss(self):
    #     print(self.host)
