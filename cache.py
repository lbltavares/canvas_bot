"""
Cache de disciplinas e tarefas.
"""
import json
import os
from datetime import datetime
from logger import LoggerFactory
from canvasapi import Canvas
import config
import pickle

_log = LoggerFactory.get_default_logger(__name__)
_log.setLevel(config.get('cache_log_level', 'INFO'))


_canvas = Canvas(
    base_url="https://pucminas.instructure.com",
    access_token=config.get('canvas_token')
)

_last_update = None
_assignments = None
_quizzes = None
_courses = None


def _update():
    global _last_update, _assignments, _quizzes, _courses
    _log.info('Atualizando cache...')
    courses = _canvas.get_courses(enrollment_state='active')

    courses_list = []
    for c in courses:
        _log.debug("-" * 50)
        courses_list.append(c)

    assignments_list = []
    quizzes_list = []
    for c in courses_list:
        _log.debug(f'Processando disciplina {c.name}')
        course_name = c.name.title()

        # Get all assignments
        assignments = c.get_assignments()
        quizzes = c.get_quizzes()
        try:
            for a in assignments:
                assignments_list.append(a)
        except:
            pass
        try:
            for q in quizzes:
                quizzes_list.append(q)
        except:
            pass

    # Escreve os arquivos de cache
    _create_cache_dir_if_not_exists()
    cache_dir = config.get('cache_dir')
    _courses = courses_list
    with open(os.path.join(cache_dir, 'courses.pickle'), 'wb') as f:
        _log.info('Escrevendo cursos...')
        pickle.dump(courses_list, f)
    _assignments = assignments_list
    with open(os.path.join(cache_dir, 'assignments.pickle'), 'wb') as f:
        _log.info('Escrevendo tarefas...')
        pickle.dump(assignments_list, f)
    _quizzes = quizzes_list
    with open(os.path.join(cache_dir, 'quizzes.pickle'), 'wb') as f:
        _log.info('Escrevendo quizzes...')
        pickle.dump(quizzes_list, f)

    _last_update = datetime.now()
    last_update_str = _last_update.strftime('%d/%m/%Y %H:%M:%S')
    with open(os.path.join(cache_dir, 'meta.json'), 'w') as f:
        _log.info('Escrevendo meta...')
        json.dump({
            'last_update': last_update_str,
            'assignments': len(_assignments),
            'quizzes': len(_quizzes),
            'courses': len(_courses)
        }, f, indent=4)
    _log.info(f'Cache atualizado em {last_update_str}.')


def _deve_atualizar():
    if _courses is None or _assignments is None or _quizzes is None:
        return True
    # Tempo desde o ultimo update em minutos
    time_since_update = (datetime.now() - _last_update).seconds / 60
    if time_since_update > config.get('cache_refresh_interval_minutes', 60):
        return True
    return False


def _create_cache_dir_if_not_exists():
    """
    Cria diretório para cache caso não exista.
    """
    os.makedirs(config.get('cache_dir'), exist_ok=True)


def update():
    """
    Atualiza o cache.
    """
    _update()


def last_update():
    """
    Retorna data da ultima atualização do cache.
    """
    return _last_update


def get_assignments() -> list:
    """
    Retorna lista de assignments.
    """
    if _deve_atualizar():
        _update()
    return _assignments


def get_quizzes() -> list:
    """
    Retorna lista de assignments.
    """
    if _deve_atualizar():
        _update()
    return _quizzes


def get_courses() -> list:
    """
    Retorna lista de assignments.
    """
    if _deve_atualizar():
        _update()
    return _courses


def init():
    global _last_update, _assignments, _quizzes, _courses
    cache_dir = config.get('cache_dir')
    if not os.path.exists(cache_dir):
        _update()
        return
    try:
        with open(os.path.join(cache_dir, 'courses.pickle'), 'rb') as f:
            _courses = pickle.load(f)
        with open(os.path.join(cache_dir, 'assignments.pickle'), 'rb') as f:
            _assignments = pickle.load(f)
        with open(os.path.join(cache_dir, 'quizzes.pickle'), 'rb') as f:
            _quizzes = pickle.load(f)
        with open(os.path.join(cache_dir, 'meta.json'), 'r') as f:
            meta = json.load(f)
            d = datetime.strptime(meta['last_update'], '%d/%m/%Y %H:%M:%S')
            _last_update = d
    except Exception as e:
        _log.error(f'Erro ao carregar cache: {e}')
        _update()


init()
