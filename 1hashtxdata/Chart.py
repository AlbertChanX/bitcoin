
import pandas as pd
import plotly   # .plotly as py
import plotly.graph_objs as go
from timetools import get_time


class Chart(object):
    @staticmethod
    def get_bar(df):
        xtime = map(lambda x: str(pd.Period(x, freq='M')), df.index.tolist())
        # print(xtime)
        trace1 = go.Bar(
            x=xtime,
            y=df['fee'].tolist(),
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
            barmode='relative',     # stack
            title='Revenue & Fee & Payoff\n updatetime:%s' % get_time()
        )

        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='revenue-fee-payoff.html')