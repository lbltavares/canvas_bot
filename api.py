import cache
from datetime import datetime as dt, timezone as tz
import config
import merger
from logger import LoggerFactory

_log = LoggerFactory.get_default_logger(__name__, filename=config.get(
    'log_filename', 'app.log') if config.get('unique_log_file') else None)
_log.setLevel(config.get('api_log_level', 'INFO'))


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
            result.append((c.name, t))
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
    # Obtem as notas de todos os quizzes e atribuições
    quizzes = cache.get_quizzes()
    assigns = cache.get_assignments()
    courses = cache.get_courses(as_dict=True)
    result = []
    for c in courses:
        # Get scores for this course
        scores = []


def set_notificar(val):
    pass
