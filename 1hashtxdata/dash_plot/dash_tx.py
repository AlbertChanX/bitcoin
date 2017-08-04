
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import logger
log = logger.get_logger('dash.py')


def application(df, df2):
    app = dash.Dash()

    app.layout = html.Div([

        html.Div([
        dcc.Graph(id='tx-graphic'),

        dcc.Slider(
            id='year--slider',
            min=df.index.year.min(),
            max=df.index.year.max(),
            value=df.index.year.max(),      # default
            step=None,
            marks={str(year): str(year) for year in df.index.year.unique()}
        )], style={'padding': '2%'}),
        html.Div([
            dcc.RadioItems(
                id='dropdown-b',
                options=[{'label': i, 'value': i} for i in ['1HASH']],
                value='1HASH'
            ),
            dcc.Graph(id='onehash-balance')
        ], style={'padding': '1%', 'height': '800px'})
        ])

    @app.callback(
        dash.dependencies.Output('tx-graphic', 'figure'),
        [
         dash.dependencies.Input('year--slider', 'value')])
    def update_graph(year_value):
        dff = df[str(year_value)]  # year_value = '2017'
        xtime = map(lambda x: str(pd.Period(x, freq='M')), dff.index)
        return {
            'data': [go.Bar(
                x=xtime,
                y=dff['fee'],
                text=(dff['fee']/dff['balance_diff']).
                  apply(lambda x: str("{0:.2f}%".format((x*100)))),
                name='Fee'

            ),
                go.Bar(
                x=xtime,
                y=dff['balance_diff'],
                name='Revenue'
            ),
                go.Bar(
                    x=xtime,
                    y=dff['payout'],
                    name='Payoff'
                )
            ],
            'layout': go.Layout(
                xaxis={
                    'title': 'time',
                    # 'type': 'linear' if xaxis_type == 'Linear' else 'log'
                },
                yaxis={
                    'title': 'BTC',
                },
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest',
                title='Revenue & Fee & Payment'
            )
        }

    @app.callback(
        dash.dependencies.Output('onehash-balance', 'figure'),
        [dash.dependencies.Input('dropdown-b', 'value')])
    def update_graph(v):
        # dff = df2[df2['Year'] == year_value]
        log.critical('balance pic')
        return {
            'data': [go.Scatter(
                x=df2['time'],
                y=df2['balance'],
                text=df2['time'],
                customdata=df2['balance'],
                name='balance'

            )],
            'layout': go.Layout(
                title='1hash Balance'
            )
        }
    app.run_server(host='0.0.0.0', use_reloader=True)  # default port=8050


# hello
