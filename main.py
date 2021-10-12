from canvas import canvas
from logger import LoggerFactory
from threading import Timer
import merger
import telegram_bot
import config
import cache
import util


_log = LoggerFactory.get_default_logger(__name__, filename=config.get(
    'log_filename', 'app.log') if config.get('unique_log_file') else None)
_log.setLevel(config.get('main_log_level', 'INFO'))


def schedule_cache_update():
    _log.info('Agendando atualizacao do cache')
    secs = config.get('cache_refresh_interval_minutes', 15) * 60
    Timer(secs, cache.update).start()


def main():
    schedule_cache_update()
    telegram_bot.init()


if __name__ == '__main__':
    main()
