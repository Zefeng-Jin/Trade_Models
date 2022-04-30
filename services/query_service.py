import pandas as pd
import pymysql
from dbutils.pooled_db import PooledDB

import config as c
from table_structure.stock import Stock


class query_service:

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
                        db='trade',
                        use_unicode=True)
        return pool

    def get_dw30(self):
        """
        获取道琼斯30股票信息
        :param market_data:
        :return:
        """
        db = self.pool.steady_connection()
        cur = db.cursor()
        sql = "SELECT STOCK_CODE, COMPANY, DOW,SP500 FROM stock WHERE Dow = true;"
        stock_list = []
        try:
            cur.execute(sql)
            results = cur.fetchall()
            for r in results:
                s = Stock()
                s.stock_code = r[0]
                s.company = r[1]
                s.dow = r[2]
                s.sp500 = r[3]
                stock_list.append(s)
            db.commit()
        except Exception as e:
            db.rollback()
            print("SQL执行错误，原因: ", e)
        finally:
            cur.close()
            db.close()
        return stock_list

    def get_sp500(self):
        """
        获取标普500股票信息
        :return:
        """
        db = self.pool.steady_connection()
        cur = db.cursor()
        sql = "SELECT STOCK_CODE, COMPANY, DOW, SP500 FROM stock WHERE SP500 = true;"
        stock_list = []
        try:
            cur.execute(sql)
            results = cur.fetchall()
            for r in results:
                s = Stock()
                s.stock_code = r[0]
                s.company = r[1]
                s.dow = r[2]
                s.sp500 = r[3]
                stock_list.append(s)
            db.commit()
        except Exception as e:
            db.rollback()
            print("SQL执行错误，原因: ", e)
        finally:
            cur.close()
            db.close()
        return stock_list

    def get_hist_market(self, stock_code):
        """
        获取历史股票行情信息
        :return:
        """
        db = self.pool.steady_connection()
        cur = db.cursor()
        sql = "select M.* from " \
              "(SELECT *  FROM market WHERE stock_code = 'AAPL' order by occur_time desc limit 500) " \
              "AS M ORDER BY M.occur_time ASC ;".format(stock_code)
        try:
            df = pd.read_sql(sql, db)
            db.commit()
        except Exception as e:
            db.rollback()
            print("SQL执行错误，原因: ", e)
        finally:
            cur.close()
            db.close()
        return df


if __name__ == '__main__':
    print(query_service().get_hist_market("AAPL"))
