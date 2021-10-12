import os

ambiente = os.environ.get('AMBIENTE') or 'dev'


class BaseConfig:
    LOG_LEVEL = 'INFO'
    DEBUG = False
    ENABLE = True


class TelegramConfig(BaseConfig):
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


class CanvasConfig(BaseConfig):
    CANVAS_URL = "https://pucminas.instructure.com"
    CANVAS_TOKEN = os.environ.get("CANVAS_TOKEN")
    IGNORAR_DISCIPLINAS = [
        6377,  # Guia Do Canvas
        25191,  # Espaço Da Coordenação
        77293,  # Trabalho de Conclusão de Curso
    ]


class LogConfig(BaseConfig):
    UNIQUE_LOG_FILE = True
    LOGS_DIR = os.path.join(os.path.dirname(__file__), 'logs')
    LOG_FILENAME = 'app'  # .log


class CacheConfig(BaseConfig):
    ENABLE = ambiente != 'dev'
    CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')
    REFRESH_INTERVAL_S = 30


class MergeConfig(BaseConfig):
    MERGE_DIR = os.path.join(os.path.dirname(__file__), 'merges')
    MERGE_MIME_CLASSES = ['pdf', 'doc']  # , 'image', 'ppt']

    # Tempo de antecedencia para o merge automatico
    TEMPO_AUTO_MERGE = 10  # em minutos

    # Intervalo de verificacao de necessidade de automerge
    CHECK_INTERVAL_M = 4


class NotifConfig(BaseConfig):
    # Horas antes de cada tarefa
    HORAS_ANTECEDENCIA = 70
    # Intervalo de verificacao de necessidade de notificacao
    CHECK_INTERVAL_M = 2
    # Numero de tarefas a serem exibidas no comando /proximas
    PROXIMAS_TAREFAS = 3


class UtilConfig(BaseConfig):
    pass


class ApiConfig(BaseConfig):
    pass


class MainConfig(BaseConfig):
    pass
