"""
Cache de disciplinas e tarefas.
"""
import os
from datetime import datetime
from logger import LoggerFactory
from canvasapi import Canvas
import config
import tarefa
import json

_log = LoggerFactory.get_default_logger(__name__)
_log.setLevel(config.get('cache_log_level', 'INFO'))


_canvas = Canvas(
    base_url="https://pucminas.instructure.com",
    access_token=config.get('canvas_token')
)

_tarefas = None
_last_update = None


def _update() -> list:
    global _last_update
    _log.info('Atualizando cache...')
    courses = _canvas.get_courses(enrollment_state='active')

    # Obtem lista de disciplinas ignoradas
    ignorar = config.get('ignorar_disciplinas', [])
    _log.debug(f'Ignorando: {ignorar}')

    tarefas = []
    for c in courses:
        _log.debug("-" * 50)
        course_name = c.name.title()
        course_id = c.id
        # Ignora disciplinas
        if course_id in ignorar:
            _log.debug(f"Skipping {course_name[:50]}...")
            continue

        # log course information
        _log.debug("Course: " + course_name)
        _log.debug("Course ID: " + str(course_id))

        # Get all assignments
        assignments = c.get_assignments()
        quizzes = c.get_quizzes()
        for a in (assignments, quizzes):
            for b in a:
                t = tarefa.from_dict(b.__dict__)
                t['course_name'] = course_name
                tarefas.append(t)
                _log.debug(tarefa.format(t))
    _last_update = datetime.now()
    _log.info(f'Cache atualizado {_last_update}')
    return tarefas


def init(do_update=False):
    """
    Inicializa o cache a partir do arquivo json ou atualiza o cache.
    """
    global _tarefas
    _log.info('Inicializando cache...')
    jfile = config.get('cache_json_file')
    jdir = os.path.dirname(jfile)
    if not os.path.exists(jdir):
        os.makedirs(jdir)
    if do_update or not os.path.isfile(jfile):
        update()
    else:
        with open(jfile, 'r') as f:
            _tarefas = json.load(f)


def update():
    """
    Atualiza o cache.
    """
    global _tarefas
    _tarefas = _update()
    with open(config.get('cache_json_file'), 'w') as f:
        json.dump(_tarefas, f, indent=4)


def last_update():
    """
    Retorna data da ultima atualização do cache.
    """
    return _last_update


def get_tarefas(filter=None) -> list:
    """
    Retorna lista de tarefas.

    :param filter: filtro para tarefas
    """
    if _tarefas is None:
        init()
    if filter is None:
        return _tarefas.copy()
    else:
        return [t for t in _tarefas if filter(t)]
