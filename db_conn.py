import pymysql
from dbutils.pooled_db import PooledDB


class dbConn:

    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.passwd = 'Sj13722449888'
        self.port = 3306
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
                        db='auto_trade',
                        use_unicode=True)
        return pool

    def insert_market(self, *args):
        """
        插入行情表
        :param args:
        :return:
        """
        db = self.pool.steady_connection()
        cur = db.cursor()
        sql = "INSERT IGNORE INTO T_MARKET " \
              "(BUSI_DATE,STOCK_CODE,OCCUR_TIME,OPEN_PRICE,HIGH_PRICE,LOW_PRICE,CLOSE_PRICE,ADJUST_CLOSE_PRICE,VOLUME) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        args = (*args,)
        try:
            cur.executemany(sql, args)
            db.commit()
        except Exception as e:
            db.rollback()
            print("SQL执行错误，原因: ", e)
        finally:
            cur.close()
            db.close()

    def insert_profit_loss(self):
        print(self.host)


