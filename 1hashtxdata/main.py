
import logger
from txinfo import Data
from chart import Chart
from dash_plot.dash_tx import application

#   /\_/\
# =( °w° )=
#   )   (  //
#  (__ __)//

if __name__ == '__main__':
    logger.initialize('DEBUG', 'INFO', 'log/tx.log')
    log = logger.get_logger('main.py')
    # update data
    v_list = Data().get_tx()
    Data().update_tx(v_list)
    # get group by excel
    df = Data().group_result(year=None)  # year='2017'

    print(df)
    application(df)
    # get Charts
    # Chart.get_bar(df)
    # Chart.get_line_bar(df)
