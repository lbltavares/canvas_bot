from logger import LoggerFactory
from threading import Timer
import config
import cache
import time


_log = LoggerFactory.get_default_logger(__name__)
_log.setLevel(config.get('main_log_level', 'INFO'))


def schedule_cache_update():
    _log.info('Scheduling cache update')
    secs = config.get('cache_refresh_interval_minutes', 15) * 60
    Timer(secs, cache.update).start()


def main():
    schedule_cache_update()

    while True:
        print('sleeping')
        time.sleep(1)


if __name__ == '__main__':
    # main()
    import api

    for p in api.proximas():
        print(f"{p} - {p.due_at_date}")
