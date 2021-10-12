import os

ambiente = os.environ.get('AMBIENTE') or 'dev'

__conf = {
    # Configuracoes de acesso
    "canvas_url": "https://pucminas.instructure.com",
    "canvas_token": os.environ.get("CANVAS_TOKEN"),
    "telegram_token": os.environ.get("TELEGRAM_TOKEN"),
    "telegram_chat_id": os.environ.get("TELEGRAM_CHAT_ID"),

    # Logs
    'unique_log_file': True,
    'logs_dir': os.path.join(os.path.dirname(__file__), 'logs'),
    'log_filename': 'app',  # .log
    'main_log_level': 'INFO',
    'cache_log_level': 'INFO',
    'merger_log_level': 'INFO',
    'canvas_log_level': 'INFO',
    'telegram_bot_log_level': 'INFO',
    'util_log_level': 'INFO',
    'api_log_level': 'INFO',

    # Disciplinas a serem ignoradas
    "ignorar_disciplinas": [
        6377,
        25191,
        77293,  # Trabalho de Conclusão de Curso
    ],

    # Cache
    # Ativa ou desativa a atualizacao do cache
    'enable_cache_refresh': ambiente != 'dev',

    # Merge
    'merge_dir': os.path.join(os.path.dirname(__file__), 'merges'),
    'merge_mime_classes': ['pdf', 'doc'],  # , 'image', 'ppt'],

    # Realiza o merge automatico de arquivos de cada tarefa
    "auto_merge": True,

    # Tempo de antecedencia para o merge automatico
    "tempo_auto_merge": 10,  # em minutos

    # Intervalo de verificacao de necessidade de automerge
    "automerge_interval_minutes": 4,


    # Tempo em minutos entre refreshs do cache
    'cache_refresh_interval_minutes': 30,
    'cache_dir': os.path.join(os.path.dirname(__file__), 'cache'),

    # Notifica quando uma tarefa estiver proxima
    "notificar": True,
    "tempo_notificacao": 15,  # Horas antes de cada tarefa

    # Intervalo de verificacao de necessidade de notificacao
    "notificacao_interval_minutes": 10,


    # Numero de tarefas a serem exibidas no comando /proximas
    "proximas_tarefas": 3,

}

# Configuracoes que podem ser modificadas
__setters = ["notificar",
             "auto_merge",
             "tempo_noficiacao",
             "tempo_merge",
             "proximas_tarefas",
             "ignorar_disciplinas"]


def get(name, default=None):
    if name in __conf:
        return __conf[name]
    else:
        return default


def set(name, value):
    if name in __setters:
        __conf[name] = value
    else:
        raise NameError(f"{name} nao pode ser modificado(a)")
    return value