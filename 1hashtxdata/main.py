
import logger
from txinfo import Data
from Chart import Chart

if __name__ == '__main__':
    logger.initialize('DEBUG', 'INFO', 'tx.log')
    log = logger.get_logger('main.py')
    # update data
    v_list = Data().get_tx()
    Data().update_tx(v_list)
    # get group by excel
    df = Data().group_result(year=None)
    # get Charts
    # print(df.index)
    # for i in df.index:
    #     print str(i)[:10]
    print(df)
    Chart.get_bar(df)
