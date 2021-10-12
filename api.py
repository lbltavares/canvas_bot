import cache
from datetime import datetime as dt, timezone as tz
import config
import merger
from logger import LoggerFactory
from telegram_bot import get_bot, send_message
from util import format_tarefa

_log = LoggerFactory.get_default_logger(__name__)
_log.setLevel(config.Api.LOG_LEVEL)


def calendario():
    pass


def proximas(limit=None):
    quizzes = cache.get_quizzes()
    assigns = cache.get_assignments()
    courses = cache.get_courses(as_dict=True)
    result = []
    for t in quizzes + assigns:
        c = courses[t.course_id]
        due_at = t.due_at
        if due_at is None:
            continue
        due_at_date = t.due_at_date
        agora = dt.now().astimezone()
        if due_at_date > agora:
            result.append((c, t))
    result = sorted(result, key=lambda x: x[1].due_at_date)
    return result[:limit]


def courses():
    courses = cache.get_courses()
    result = []
    for c in courses:
        name = c.name.split('-')[0]
        name = name.strip().title()
        result.append((name, c.id))
    return result


def merge(course_id, start_download_cb=None, end_download_cb=None, start_merge_cb=None, end_merge_cb=None):

    course = cache.get_courses(as_dict=True).get(course_id)
    if course is None:
        raise ValueError(f'ID nao encontrado: {course_id}')

    start_download_cb(course) if start_download_cb is not None else None

    files = merger.download_files(course)

    end_download_cb(course, files) if end_download_cb is not None else None
    start_merge_cb(course) if start_merge_cb is not None else None

    result = merger.merge(course)

    end_merge_cb(course) if end_merge_cb is not None else None

    return result


def pontos():
    pass


def set_notificar(val):
    pass


def notificar():
    if not config.Notif.ENABLE:
        _log.info('Pulando notificacao')
        return
    prox = proximas(limit=1)
    if not prox or len(prox) == 0:
        return
    _log.info("Verificando notificacao")
    c, t = prox[0]
    agora = dt.now().replace(tzinfo=tz.utc)
    secs = (t.due_at_date - agora).total_seconds()
    m = secs / 60
    if m > config.Notif.ANTECEDENCIA_M:
        return
    _log.info("Notificando...")
    msg = "A seguinte tarefa está proxima:\n\n"
    msg += format_tarefa(t, c.name)
    send_message(msg)


def automerge():
    if not config.Merge.ENABLE:
        _log.info('Pulando auto_merge')
        return
    prox = proximas(limit=1)
    if not prox or len(prox) == 0:
        return
    c, t = prox[0]
    agora = dt.now().astimezone()
    secs = (t.due_at_date - agora).total_seconds()
    mins = int(secs / 60)
    if mins > config.Merge.ANTECEDENCIA_M:
        return
    result = merge(
        c.id,
        start_download_cb=lambda c: send_message(
            f'Baixando arquivos de: {c.name.split("-")[0].title()}'),
        end_download_cb=lambda c, f: send_message(
            f'Download concluido. Total: {len(f)} arquivos.'),
        start_merge_cb=lambda c: send_message(
            f'Iniciando o merge...'),
        end_merge_cb=lambda c: send_message(
            f'Merge finalizado com sucesso.')
    )
    try:
        fpath = result['merge_path']
        fname = result['merge_filename']
        files_merged = result['files_merged']
        files_merged = [f[:45] + '...' + f[-5:]
                        if len(f) > 50
                        else f
                        for f in files_merged]
        files_merged = '\n'.join(files_merged)
        msg = "Arquivos que foram juntados:\n" + files_merged
        send_message(msg)
        get_bot().send_document(
            chat_id=config.TELEGRAM_CHAT_ID,
            document=open(fpath, 'rb'),
            filename=fname
        )
    except Exception as e:
        send_message(f"Erro: {e}")
