# from __future__ import unicode_literals

# print '\'xxx\' is unicode?', isinstance('xxx', unicode)
# print 'u\'xxx\' is unicode?', isinstance(u'xxx', unicode)
# print '\'xxx\' is str?', isinstance('xxx', str)
# print 'b\'xxx\' is str?', isinstance(b'xxx', str)

import pandas as pd
from pandas_datareader import data, wb
import pandas_datareader as pdr
import datetime

start = datetime.datetime(2016,1,1)
end = datetime.date.today()

apple = pdr.get_data_sina("AAPL", start, end)

type(apple)