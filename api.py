
import os
import cache
from cache import get_course_dir
from datetime import datetime as dt, timezone as tz
import config
import merger
from logger import LoggerFactory
from telegram_bot import get_bot, send_message
from util import format_tarefa

_log = LoggerFactory.get_default_logger(__name__)
_log.setLevel(config.Api.LOG_LEVEL)

notificacoes = []
automerges = []


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


def download_course_files(course_id):
    course = cache.get_courses(as_dict=True)[course_id]
    course_files = course.get_files()
    course_dir = get_course_dir(course)
    os.makedirs(course_dir, exist_ok=True)

    baixados = []
    for f in course_files:
        try:
            fname = f.filename
            fpath = os.path.join(course_dir, fname)
            fsize = f.size
            if os.path.exists(fpath) and os.path.getsize(fpath) == fsize:
                _log.info(
                    f'Arquivo ja baixado: {fname}')
                continue
            _log.info(f'Baixando arquivo: {fname} ({fsize / 1024 / 1024}mb)')
            f.download(fpath)
            baixados.append(fpath)
        except Exception as e:
            _log.exception(f'Erro ao baixar arquivo: {fname}')

    return baixados


def convert_course_files_to_pdf(course_id):
    course = cache.get_courses(as_dict=True)[course_id]
    course_dir = merger.get_course_dir(course)
    files = merger.convert_to_pdf(course_dir)
    return files


def merge_course_pdf_files(course_id):
    course = cache.get_courses(as_dict=True)[course_id]
    course_pdf_dir = merger.get_course_dir(course)
    course_pdf_dir = os.path.join(course_pdf_dir, 'pdf')
    cname = course.name.split('-')[0].strip().title()
    cname = [c for c in cname if c.isalnum() or c in ['.', ' ']]
    cname = ''.join(cname)
    cname = cname.replace(' ', '_')
    dest_file = os.path.join(course_pdf_dir, f'{cname}_merged.pdf')
    files = merger.merge_dir(course_pdf_dir, dest_file)
    return (dest_file, files)


def merge(course_id, start_download_cb=None, end_download_cb=None,
          start_conversion_cb=None, end_conversion_cb=None,
          start_merge_cb=None, end_merge_cb=None):

    course = cache.get_courses(as_dict=True).get(course_id)
    if course is None:
        raise ValueError(f'ID nao encontrado: {course_id}')

    course_dir = merger.get_course_dir(course)
    start_download_cb(course) if start_download_cb is not None else None
    files = download_course_files(course_id)
    end_download_cb(course, files) if end_download_cb is not None else None

    start_conversion_cb(course) if start_conversion_cb is not None else None
    conv_files = merger.convert_to_pdf(course_dir)
    end_conversion_cb(
        course, conv_files) if end_conversion_cb is not None else None

    start_merge_cb(course) if start_merge_cb is not None else None
    result = merger.merge(course)
    end_merge_cb(course) if end_merge_cb is not None else None

    return result


def pontos():
    pass


def notificar():
    if not config.Notif.ENABLE:
        _log.info('Pulando notificacao')
        return
    if len(notificacoes) > 100:
        notificacoes.clear()
    prox = proximas()
    if not prox or len(prox) == 0:
        return
    _log.info("Verificando notificacao")
    for c, t in prox:
        if t.id in notificacoes:
            continue
        agora = dt.now().replace(tzinfo=tz.utc)
        secs = (t.due_at_date - agora).total_seconds()
        mins = int(secs / 60)
        if mins > config.Notif.ANTECEDENCIA_M:
            continue
        _log.info("Notificando...")
        msg = "A seguinte tarefa está proxima:\n\n"
        msg += format_tarefa(t, c.name)
        send_message(msg)
        notificacoes.append(t.id)


def automerge():
    if not config.Merge.ENABLE:
        _log.info('Pulando auto_merge')
        return
    if len(automerges) > 100:
        automerges.clear()
    prox = proximas()
    if not prox or len(prox) == 0:
        return
    for c, t in prox:
        if t.id in automerges:
            return
        agora = dt.now().replace(tzinfo=tz.utc)
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
            msg = "Arquivos do merge:\n" + files_merged
            send_message(msg)
            get_bot().send_document(
                chat_id=config.TELEGRAM_CHAT_ID,
                document=open(fpath, 'rb'),
                filename=fname
            )
            automerges.append(t.id)
        except Exception as e:
            send_message(f"Erro: {e}")
