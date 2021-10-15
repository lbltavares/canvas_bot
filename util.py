"""
    Utilitarios
"""

from datetime import datetime as dt
import re
import locale
import config

from logger import LoggerFactory

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

_log = LoggerFactory.get_default_logger(__name__)
_log.setLevel(config.Util.LOG_LEVEL)


def format_tarefa(tarefa, course_name=None):
    """Retorna uma string formatada da tarefa"""
    # Course Name
    if course_name:
        course_name = course_name.split('-')[0].strip().title()

    # Nome
    name = getattr(tarefa, 'name', None)
    name = getattr(tarefa, 'title', name)
    if name:
        name = name.title().strip()

    # Datas
    due_at = tarefa.due_at
    due_at_date = None
    faltam = None
    passou = None
    if due_at:
        # America/Sao_Paulo
        due_at_date = tarefa.due_at_date.astimezone()
        agora = dt.now().astimezone()
        faltam = (due_at_date - agora).days
        passou = faltam < 0
        due_at = due_at_date.strftime('%a, %d %b %Y - %H:%M:%S')

    # Descricao
    desc = parse_description(getattr(tarefa, 'description', None))
    desc = desc[:50]+'...' if desc else None

    result = ""
    if course_name:
        result += f"{course_name}\n"
    if name:
        result += f"{name}\n"
    if getattr(tarefa, 'id', None):
        result += f"{tarefa.id}\n"
    if desc:
        result += f"Desc: {desc}\n"
    if due_at:
        result += f"Prazo: {due_at}\n"
    if faltam is not None and faltam >= 0:
        if faltam <= 1:
            result += '\U0001F534 '
        elif faltam <= 2:
            result += '\U0001F7E0 '
        result += f"Faltam: {faltam} dia(s)\n"
    if passou:
        result += f"Passou: {passou}\n"
    if getattr(tarefa, 'question_count', None):
        result += f"Questoes: {tarefa.question_count}\n"
    if getattr(tarefa, 'points_possible', None):
        result += f"Pontos: {tarefa.points_possible}\n"
    if getattr(tarefa, 'html_url', None):
        result += f"{tarefa.html_url}\n"

    return result


def parse_description(description):
    """Retorna a descricao sem tags de HTML, espaços repetidos e URL formatadas"""
    if description:
        description = re.sub(r'<[^>]*>', '', description)
        description = re.sub(r'(&nbsp|&amp|&quot|&lt|&gt)', '', description)
        description = re.sub(r'\s+', ' ', description)
        description = re.sub(r'https?://[^\s]+', '', description)
    return description
