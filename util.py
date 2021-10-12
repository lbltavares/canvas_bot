import re
import locale
import config
from datetime import datetime as dt, timezone

from logger import LoggerFactory

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

_log = LoggerFactory.get_default_logger(__name__)
_log.setLevel(config.UtilConfig.LOG_LEVEL)


def format_tarefa(t, course_name=None):
    # Course Name
    if course_name:
        course_name = course_name.split('-')[0].strip().title()

    # Nome
    name = getattr(t, 'name', None)
    name = getattr(t, 'title', name)
    if name:
        name = name.title().strip()

    # Datas
    due_at = t.due_at
    due_at_date = None
    faltam = None
    passou = None
    if due_at:
        # America/Sao_Paulo
        due_at_date = t.due_at_date.astimezone()
        agora = dt.now().astimezone()
        faltam = (due_at_date - agora).days
        passou = faltam < 0
        due_at = due_at_date.strftime('%a, %d %b %Y - %H:%M:%S')

    # Descricao
    desc = parse_description(getattr(t, 'description', None))
    desc = desc[:50]+'...' if desc else None

    result = ""
    if course_name:
        result += f"{course_name}\n"
    if name:
        result += f"{name}\n"
    if getattr(t, 'id', None):
        result += f"{t.id}\n"
    if desc:
        result += f"Desc: {desc}\n"
    if due_at:
        result += f"Prazo: {due_at}\n"
    if faltam != None and faltam >= 0:
        result += f"Faltam: {faltam} dia(s)\n"
    if passou:
        result += f"Passou: {passou}\n"
    if getattr(t, 'question_count', None):
        result += f"Questoes: {t.question_count}\n"
    if getattr(t, 'points_possible', None):
        result += f"Pontos: {t.points_possible}\n"
    if getattr(t, 'html_url', None):
        result += f"{t.html_url}\n"

    return result


def parse_description(d):
    if d:
        d = re.sub(r'<[^>]*>', '', d)
        d = re.sub(r'(&nbsp|&amp|&quot|&lt|&gt)', '', d)
        d = re.sub(r'\s+', ' ', d)
        d = re.sub(r'https?://[^\s]+', '', d)
    return d
