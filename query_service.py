import pymysql
from dbutils.pooled_db import PooledDB
import subscribe_service as ss


class push_service:

    def __init__(self):
        self.host = 'sh-cynosdbmysql-grp-o8wcogew.sql.tencentcdb.com'
        self.user = 'root'
        self.passwd = 'Sj13722449888'
        self.port = 25897
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
                        db='trade',
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
        :param market_data:
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
    #
    # def insert_profit_loss(self):
    #     print(self.host)


if __name__ == '__main__':
    data_data = ss.subscribe_stocks_list()
    push_service().insert_stocks(data_data)
