"""
    main.py
    ~~~~~~~~~~~~~~
"""

from apscheduler.schedulers.background import BackgroundScheduler
from api import automerge, notificar
from cache import atualizar
from logger import LoggerFactory
import telegram_bot
import config


_log = LoggerFactory.get_default_logger(__name__)
_log.setLevel(config.Main.LOG_LEVEL)


if __name__ == '__main__':
    _sched = BackgroundScheduler(timezone='America/Sao_Paulo')
    _log.info("Agendando tarefas...")
    _sched.add_job(atualizar, 'cron',
                   minute=f'*/{config.Cache.REFRESH_INTERVAL_M}')
    _sched.add_job(notificar, 'cron',
                   minute=f'*/{config.Notif.CHECK_INTERVAL_M}')
    _sched.add_job(automerge, 'cron',
                   minute=f'*/{config.Merge.CHECK_INTERVAL_M}')
    _sched.start()
    _log.info('Iniciado.')
    telegram_bot.init()
