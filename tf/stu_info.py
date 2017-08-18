# coding:utf-8
# python3
import pandas as pd
import time


df = pd.read_excel('/Users/cyc/Downloads/exam.xls')
print(df.columns)
df.columns = ['exam_name', 'grade', 'stuid', 'name','sex', 'id', 'major', 'class']
df = df.set_index('stuid')
df = df[['name', 'sex', 'id', 'major', 'grade']]

# print(df.duplicated())

df = df.drop_duplicates()
print(df)
# [(df['grade'] == 2013) & (df['sex'] == '女')]
df['psw'] = df['id'].apply(lambda x: str(x)[-6:])

print((df['psw']))

from selenium import webdriver
driver = webdriver.PhantomJS()

u1 = 'http://www.okcoin.cn'
url = 'http://www.zstu.edu.cn/'
c = driver.get(url)
time.sleep(3)
driver.save_screenshot('screenie.png')
driver.close()
