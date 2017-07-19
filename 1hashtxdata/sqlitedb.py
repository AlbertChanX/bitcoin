
import DBHelper
import sqlite3
import pandas as pd

conn = sqlite3.connect('tx.db')


# conn.execute('''
#              DROP TABLE IF exists income;
#  ''')
# conn.execute('''CREATE TABLE INCOME
#         (ID            INTEGER PRIMARY KEY,
#         time           TEXT    NOT NULL,
#         txid           text    NOT NULL,
#         balance_diff   float   NOT NULL,
#         fee            float   NOT NULL,
#         is_coinbase     int    NOT NULL,
#         outputs_count   int    NOT NULL);
#         ''')
#
# conn.execute('''CREATE INDEX index_time
#        ON income (time);''')
# conn.execute('''CREATE TABLE PAYOUT
#        (ID INT PRIMARY KEY     NOT NULL,
#        time           TEXT    NOT NULL,
#        txid           TEXT     NOT NULL,
#        tx_value         decimal(12,8));''')
# insert into income values (0,'2016-02-19 18:42:38',0,0,0,0,0) ;
sql = 'select * from income'
# print conn.execute(sql).fetchall()
#
df = pd.read_sql(sql, conn)  # index_col=['id','time']
df = df.set_index(pd.DatetimeIndex(df['time']))
# pd.io.sql.write_frame(df, 'tablename', conn)
conn.close()
# df_s = df.sort_index(ascending=False)   # sort --> df_s
df_s = df[['time', 'fee']]  # .groupby(['is_coinbase']).cumsum()
# key = lambda x: x.year
# grouped = df_s.groupby(key).sum()
# print(grouped)
# grouper = pd.TimeGrouper("1M")
# df_s['sum1'] = df_s.groupby(grouper).transform(lambda x: x.sum())
print(df_s.ix[:, 'fee'].head())

# writer = pd.ExcelWriter('1hash_tx_dada_%s.xlsx' % get_time())
# df_s.to_excel(writer, 'Sheet1')  # sheet_name='Sheet1'
# writer.save()

# # print conn.execute('insert into income (time, quantity, block_revenue, fee) values (1, 2,3,4)')
# conn.commit()
# conn.close()

