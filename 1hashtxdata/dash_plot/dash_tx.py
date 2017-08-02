
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd


def application(df):
    app = dash.Dash()

    app.layout = html.Div([


        dcc.Graph(id='tx-graphic'),

        dcc.Slider(
            id='year--slider',
            min=df.index.year.min(),
            max=df.index.year.max(),
            value=df.index.year.max(),      # default
            step=None,
            marks={str(year): str(year) for year in df.index.year.unique()}
        )
    ], style={'padding': '2%'})


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
                # mode='markers',
                # marker={
                #     'size': 15,
                #     'opacity': 0.5,
                #     'line': {'width': 0.5, 'color': 'white'}
                # }
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
                hovermode='closest'
            )
        }

    app.run_server()
