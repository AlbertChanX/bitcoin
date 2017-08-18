import plotly
plotly.tools.set_credentials_file(username='githubcyc', api_key='u3eGZhI8K7hCemiAi7A7')
import time
import plotly.plotly as py
from plotly.graph_objs import *

trace0 = Scatter(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17]
)
trace1 = Scatter(
    x=[1, 2, 3, 4],
    y=[16, 5, 11, 9]
)
data = Data([trace0, trace1])

# py.plot(data, filename = 'basic-line')

import plotly

t = time.time()
plotly.offline.plot({
    "data": [Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
    "layout": Layout(title="hello world")
}, filename='test.html', auto_open=False, image='jpeg')
print('interval ', time.time()-t)



