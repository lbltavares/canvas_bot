from api import automerge, notificar
from cache import atualizar
from logger import LoggerFactory
from threading import Timer
import telegram_bot
import config


_log = LoggerFactory.get_default_logger(__name__)
_log.setLevel(config.MainConfig.LOG_LEVEL)


def agendar(immediate=False, func=None, tempo=10):
    if immediate and func:
        func()
    Timer(tempo, agendar, (True, func, tempo)).start()


def main():
    _log.info("Agendando tarefas...")
    agendar(func=atualizar, tempo=config.CacheConfig.REFRESH_INTERVAL_S * 60)
    agendar(func=notificar, tempo=config.NotifConfig.CHECK_INTERVAL_M * 60)
    agendar(func=automerge, tempo=config.MergeConfig.CHECK_INTERVAL_M * 60)
    _log.info('Iniciado.')
    telegram_bot.init()


if __name__ == '__main__':
    main()
