
import pandas as pd
import plotly
import plotly.graph_objs as go
from timetools import get_time
import numpy as np


class Chart(object):
    @staticmethod
    def get_bar(df):
        xtime = map(lambda x: str(pd.Period(x, freq='M')), df.index.tolist())
        # print(xtime)
        trace1 = go.Bar(
            x=xtime,
            y=df['fee'].tolist(),
            # percentage
            # f=df['percent'].str.strip("%").astype(float) / 100;
            text=(df['fee']/df['balance_diff']).
                  apply(lambda x: str("{0:.2f}%".format((x*100)))).tolist(),  # 0: -> x*100
            name='Fee'
        )
        trace2 = go.Bar(
            x=xtime,
            y=df['balance_diff'].tolist(),
            name='Revenue'
        )
        trace3 = go.Bar(
            x=xtime,
            y=df['payout'].tolist(),
            name='Payoff'
        )
        data = [trace1, trace2, trace3]
        layout = go.Layout(
            barmode='group',     # stack
            title='Revenue & Fee & Payoff'
        )

        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='data/revenue-fee-payoff.html',
                            link_text='updatetime:%s' % get_time())

    @staticmethod
    def get_line_bar(df):
        # df['is_coinbase'].plot(kind='bar', filename='grouped-bar-chart.html')
        xtime = map(lambda x: str(pd.Period(x, freq='M')), df.index.tolist())
        trace1 = go.Scatter(
            x=df['time'],
            y=df['balance'].tolist(),
            name='balance'
        )
        trace2 = go.Bar(
            # x=xtime,
            # y=df['balance'].tolist(),
            # name='blocks'
        )
        data = [trace1, trace2]
        layout = go.Layout(
            barmode='relative',  # stack
            title='Blocks Monthly'
        )
        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='data/Blocks-Monthly.html',
                            link_text='updatetime:%s' % get_time())

    @staticmethod
    def test():
        df = pd.DataFrame(np.random.rand(10, 4), columns=['A', 'B', 'C', 'D'])
        row = df.ix[1]
        print(row)
        row.plot(kind='bar')

if __name__ == '__main__':
    Chart.test()


