from api import automerge, notificar
from cache import update
from canvas import canvas
from logger import LoggerFactory
from threading import Timer
import telegram_bot
import config


_log = LoggerFactory.get_default_logger(__name__, filename=config.get(
    'log_filename', 'app.log') if config.get('unique_log_file') else None)
_log.setLevel(config.get('main_log_level', 'INFO'))


def agendar_cache_refresh():
    _log.info('Agendando atualizacao do cache...')
    secs = config.get('cache_refresh_interval_minutes', 15) * 60
    Timer(secs, update).start()


def agendar_notificacoes():
    _log.info('Agendando notificacoes...')
    secs = config.get('notificacoes_interval_minutes', 15) * 60
    Timer(secs, notificar).start()


def agendar_automerges():
    _log.info('Agendando automerge...')
    secs = config.get('automerge_interval_minutes', 15) * 60
    Timer(secs, automerge).start()


def main():
    agendar_cache_refresh()
    agendar_notificacoes()
    agendar_automerges()
    _log.info('Iniciado.')
    telegram_bot.init()


if __name__ == '__main__':
    main()
