import os

ambiente = os.environ.get('AMBIENTE') or 'prod'


class BaseConfig:
    DEBUG = False
    LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'
    ENABLE = True


class Telegram(BaseConfig):
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
    # Numero de tarefas a serem exibidas no comando /proximas
    PROXIMAS_TAREFAS = 3


class Canvas(BaseConfig):
    CANVAS_URL = "https://pucminas.instructure.com"
    CANVAS_TOKEN = os.environ.get("CANVAS_TOKEN")
    IGNORAR_DISCIPLINAS = [
        6377,  # Guia Do Canvas
        25191,  # Espaço Da Coordenação
        77293,  # Trabalho de Conclusão de Curso
    ]


class Log(BaseConfig):
    UNIQUE_LOG_FILE = True
    LOGS_DIR = os.path.join(os.path.dirname(__file__), 'logs')
    LOG_FILENAME = 'app'  # .log


class Cache(BaseConfig):
    ENABLE = ambiente != 'dev'
    CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')
    REFRESH_INTERVAL_M = 30  # minutos


class Merge(BaseConfig):
    MERGE_DIR = os.path.join(os.path.dirname(__file__), 'merges')
    MIME_CLASS = ['pdf', 'doc']  # , 'image', 'ppt']

    # Minutos de antecedencia antes de cada tarefa para o merge automatico
    ANTECEDENCIA_M = 50  # minutos

    # Intervalo de verificacao de necessidade de automerge
    CHECK_INTERVAL_M = 5  # a cada 30 minutos


class Notif(BaseConfig):
    # Minutos de antecedencia antes de cada tarefa
    ANTECEDENCIA_M = 20 * 60  # 20 horas

    # Intervalo de verificacao
    CHECK_INTERVAL_M = 5  # a cada 30 minutos


class Util(BaseConfig):
    pass


class Api(BaseConfig):
    pass


class Main(BaseConfig):
    pass
