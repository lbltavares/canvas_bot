import cache
from datetime import datetime, timedelta, timezone


def calendario():
    pass


def proximas(limit=1):
    quizzes = cache.get_quizzes()
    assigns = cache.get_assignments()
    for t in quizzes + assigns:
        print(t)
    return t


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
