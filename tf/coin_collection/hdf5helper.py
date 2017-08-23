import pandas as pd
import io

pd.set_option('io.hdf.default_format', 'table')


class hdf5helper(object):
    def __init__(self):

        self.store = pd.HDFStore('h5/COINS.h5', 'a')

    def get_df(self, name, filter_exp=None):  # like "columns=['region']"
        return self.store.select(name, filter_exp)

    def save_df(self, name, df):
        self.store.append(name, df, format='table', data_columns=True)

    def put_df(self, name, df):
        self.store.put(name, df, format='table', data_columns=True)

if __name__ == '__main__':
    h = hdf5helper()
    import numpy as np
    df = pd.DataFrame({'col1':[0, np.nan, 2], 'col2':[1, np.nan, np.nan]})
    # h.save_df('test', df)
    print(h.get_df('coin', filter_exp="name==yunbianscny"))
