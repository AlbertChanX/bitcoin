import logger
from wxpy import Bot
from wechat_sender import listen

log = logger.get_logger('run_msg.py')


def start_wx():
    bot = Bot(cache_path=True)
    log.info('wechat listening')
    print('OK')
    # http://wechat-sender.readthedocs.io/zh_CN/latest/listen.html#id1
    listen(bot, status_report=True)
