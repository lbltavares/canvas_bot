"""
Cache de disciplinas e tarefas.
"""
import json
import os
from datetime import datetime

import canvasapi
from logger import LoggerFactory
from canvas import canvas
import config
import pickle

_log = LoggerFactory.get_default_logger(__name__)
_log.setLevel(config.Cache.LOG_LEVEL)


_last_update = None
_assignments = None
_quizzes = None
_courses = None


def last_update_formatted():
    return _last_update.strftime('%d/%m/%Y %H:%M:%S')


def last_update():
    """
    Retorna data da ultima atualização do cache.
    """
    return _last_update


def _atualizar():
    global _last_update, _assignments, _quizzes, _courses
    if not config.Cache.ENABLE:
        _log.warning(f'Pulando atualizacao do cache')
        if _last_update:
            last = last_update_formatted()
            _log.warning(f'Ultima atualizacao: {last}')
        return

    _log.info('Atualizando cache...')
    courses = canvas.get_courses(enrollment_state='active')

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
    cache_dir = config.Cache.CACHE_DIR
    with open(os.path.join(cache_dir, 'courses.pickle'), 'wb') as f:
        _log.info('Escrevendo cursos...')
        pickle.dump(courses_list, f)
    with open(os.path.join(cache_dir, 'assignments.pickle'), 'wb') as f:
        _log.info('Escrevendo tarefas...')
        pickle.dump(assignments_list, f)
    with open(os.path.join(cache_dir, 'quizzes.pickle'), 'wb') as f:
        _log.info('Escrevendo quizzes...')
        pickle.dump(quizzes_list, f)

    _courses = courses_list
    _assignments = assignments_list
    _quizzes = quizzes_list
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
    if time_since_update > config.Cache.REFRESH_INTERVAL_M:
        return True
    return False


def _create_cache_dir_if_not_exists():
    """
    Cria diretório para cache caso não exista.
    """
    os.makedirs(config.Cache.CACHE_DIR, exist_ok=True)


def atualizar():
    """
    Atualiza o cache.
    """
    _atualizar()


def get_course_dir(c: canvasapi.course.Course) -> str:
    cname = c.name.split('-')[0].strip().replace(' ', '_').title()
    return os.path.join(config.Merge.MERGE_DIR, cname)


def get_assignments(filter=None, as_dict=False) -> list:
    """
    Retorna lista de tarefas.
    """
    if _deve_atualizar():
        _atualizar()
    ignorar = config.Canvas.IGNORAR_DISCIPLINAS
    assignments = [a for a in _assignments if a.course_id not in ignorar]
    if as_dict:
        return {a.id: a for a in assignments if filter is None or filter(a)}
    return [a for a in assignments if filter is None or filter(a)]


def get_quizzes(filter=None, as_dict=False) -> list:
    """
    Retorna lista de testes.
    """
    if _deve_atualizar():
        _atualizar()
    ignorar = config.Canvas.IGNORAR_DISCIPLINAS
    quizzes = [q for q in _quizzes if q.course_id not in ignorar]
    if as_dict:
        return {q.id: q for q in quizzes if filter is None or filter(q)}
    return [q for q in quizzes if filter is None or filter(q)]


def get_courses(filter=None, as_dict=False) -> list:
    """
    Retorna lista de cursos.
    """
    if _deve_atualizar():
        _atualizar()
    ignorar = config.Canvas.IGNORAR_DISCIPLINAS
    courses = [c for c in _courses if c.id not in ignorar]
    if as_dict:
        return {c.id: c for c in courses if filter is None or filter(c)}
    return [c for c in courses if filter is None or filter(c)]


def init():
    global _last_update, _assignments, _quizzes, _courses
    cache_dir = config.Cache.CACHE_DIR
    if not os.path.exists(cache_dir):
        _atualizar()
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
        _atualizar()


init()
