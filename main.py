from logger import LoggerFactory
import schedule
import config
import cache
import time

_log = LoggerFactory.get_default_logger(__name__)
_log.setLevel(config.get('main_log_level', 'INFO'))


def schedule_cache_update():
    _log.info('Scheduling cache update')
    cache.init(do_update=True)
    interval = config.get('cache_refresh_interval_minutes', 15)
    schedule.every(interval).minutes.do(cache.update)


def main():
    schedule_cache_update()
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
