# coding:utf-8
import sqlite3
import logger
from contextlib import contextmanager

log = logger.get_logger('DBHelper')


class DBHelper(object):
    def __init__(self):
        try:
            self.con = sqlite3.connect('tx.db')
            log.info('connected sqlite3 success')

        except sqlite3.Error, e:
            log.error('sqlite3self.connection error: %s' % e)

    # for pandas read_sql
    def get_con(self):
        return self.con

    @contextmanager
    def connector(self):
        print("connecting to sqlite3")
        con = self.con
        cur = con.cursor()
        yield cur
        print("closing connection")
        cur.close()
        con.close()

    # 查询方法，使用con.cursor(MySQLdb.cursors.DictCursor),返回结果为字典
    def select(self, sql):
        with DBHelper.connector(self) as cur:
            cur.execute(sql)
            fc = cur.fetchall()
            return fc

    def batch_insert(self, sql, value_list):  # value_list list[tuple]
        try:
            cur = self.con.cursor()
            print(sql)
            count = cur.executemany(sql, value_list)
            self.con.commit()
            log.info('batch_insert success: %s, %s' % (count, sql))
            return count
        except sqlite3.Error, e:
            cur.close()
            self.con.close()
            log.error("sqlite3 Error: %s" % e)

    # update with params
    # eg:sql='insert into test values(%s,%s,%s,now())',params=(6,'C#','good book')

    def updateByParam(self, sql, params):
        try:
            cur = self.con.cursor()
            count = cur.execute(sql, params)
            self.con.commit()
            log.info('update success: {}{}'.format(sql, params))
            return count
        except sqlite3.Error, e:
            self.con.rollback()
            cur.close()
            self.con.close()
            log.error("sqlite3 Error: %s" % e)

    # update with sql

    def update(self, sql):
        try:
            cur = self.con.cursor()
            count = cur.execute(sql)
            self.con.commit()
            log.info('update is ok: ' + sql)
            return count
        except sqlite3.Error, e:
            cur.close()
            self.con.close()
            self.con.rollback()
            log.error("sqlite3 Error: %s" % e)


# DBHelper().get_Con()
if __name__ == '__main__':
    from contextlib import closing
    import urllib

    with closing(urllib.urlopen('http://www.python.org')) as page:
        data = page.read()

        for line in page:
            print(len(line))
        # try:
        #     yield thing
        # finally:
        #     page.close()
