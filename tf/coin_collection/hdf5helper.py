import pandas as pd
import io
import logger
import tables as tb
from wechat_sender import Sender

pd.set_option('io.hdf.default_format', 'table')

log = logger.get_logger('hdf5helper.py')


class Hdf5helper(object):
    def __init__(self):
        self.store = pd.HDFStore('h5/COINS.h5', 'a')
        # self.store.remove('coin')
        # log.info(self.store['coins/yunbiethcny'])
        keys = self.store.keys()
        log.info(keys)
        log.info(self.store.get_node('coins'))   # get sub node
        log.info(self.store.get_storer('coins/yunbianscny').nrows)
        Sender().send(keys[0])

    def get_store(self):
        return self.store

    def get_df(self, name, filter_exp=None):  # like "columns=['region']"

        # store.keys()
        with pd.HDFStore('h5/COINS.h5', 'a') as store:
            return store.select(name, filter_exp)

    def save_df(self, name, df):
        self.store.append(name, df, format='table', min_itemsize={'name': 20},
                          data_columns=True)
        log.info('append success')
        self.store.close()

    # not append
    def put_df(self, name, df):
        self.store.put(name, df, format='table', min_itemsize={'name': 20},
                       data_columns=True)
        self.store.close()
        log.info('put_df success')

if __name__ == '__main__':
    h = Hdf5helper()
    import numpy as np
    df = pd.DataFrame({'col1':[0, np.nan, 2], 'col2':[1, np.nan, np.nan]})
    # h.save_df('test', df)
    try:
        print(h.get_df('coin', filter_exp="name==yunbianscny").drop_duplicates())
    except KeyError:
        pass

    f1 = tb.open_file('h5/COIN.h5', 'w')
    # for array in f1.walk_groups(where='/coins'):
    #     print(array)
    f1.close()


