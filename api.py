import cache
from datetime import datetime as dt, timezone as tz


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


def all():
    pass


def courses():
    pass


def merge(course_id):
    pass


def pontos():
    pass


def update():
    pass


def set_notificar(val):
    pass
