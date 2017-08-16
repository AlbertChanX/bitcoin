
import dbhelper
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
# conn.execute('''CREATE TABLE BLOCK
#        (ID            INT PRIMARY KEY    ,
#        time           TEXT    NOT NULL,
#        quantity       int     NOT NULL,
#        is_update      int     NOT NULL);''')
# conn.execute('''CREATE INDEX block_time
#        ON BLOCK (time);''')
# insert into income values (0,'2016-02-19 00:00:00',0,0,0,0,0) ;
sql = 'select time from income where is_coinbase=1 limit 2'
for i in (conn.execute(sql).fetchall()):
    print(''.join(i))
#
df = pd.read_sql(sql, conn)  # index_col=['id','time']

df = df.set_index(pd.DatetimeIndex(df['time']))
for i in df.index:
    print i
# print(df.index.year.unique())
# print(df['2017'])
# pd.io.sql.write_frame(df, 'tablename', conn)
conn.close()
# df_s = df.sort_index(ascending=False)   # sort --> df_s
# df_s = df[['time', 'fee']]  # .groupby(['is_coinbase']).cumsum()
# key = lambda x: x.year
# grouped = df_s.groupby(key).sum()
# print(grouped)
# grouper = pd.TimeGrouper("1M")
# df_s['sum1'] = df_s.groupby(grouper).transform(lambda x: x.sum())
# df_s.loc[:, 'fee'].head()

# writer = pd.ExcelWriter('1hash_tx_dada_%s.xlsx' % get_time())
# df_s.to_excel(writer, 'Sheet1')  # sheet_name='Sheet1'
# writer.save()

# # print conn.execute('insert into income (time, quantity, block_revenue, fee) values (1, 2,3,4)')
# conn.commit()
# conn.close()

