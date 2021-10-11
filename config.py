import os


__conf = {
    'logs_dir': os.path.join(os.path.dirname(__file__), 'logs'),

    'main_log_level': 'INFO',  # main log level

    # Disciplinas a serem ignoradas
    "ignorar_disciplinas": [
        6377,
        25191,
        77293,  # Trabalho de Conclusão de Curso
    ],

    # Cache
    'cache_refresh_interval_minutes': 15,  # Tempo em minutos entre updates
    'cache_json_file': os.path.join(os.path.dirname(__file__), 'cache', 'tarefas.json'),
    'cache_log_level': 'INFO',

    # Notifica quando uma tarefa estiver proxima
    "notificar": True,
    "tempo_notificacao": 15,  # Horas antes de cada tarefa

    # Realiza o merge automatico de arquivos de cada tarefa
    "merge": True,
    "tempo_merge": 10,  # Minutos antes de cada tarefa

    # Numero de tarefas a serem exibidas no comando /proximas
    "proximas_tarefas": 3,

    # Configuracoes de acesso
    "canvas_token": os.environ.get("CANVAS_TOKEN", ""),
    "telegram_token": os.environ.get("TELEGRAM_TOKEN", ""),
}

# Configuracoes que podem ser modificadas
__setters = ["notificar",
             "tempo_noficiacao",
             "merge",
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
