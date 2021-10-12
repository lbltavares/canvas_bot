import config
from canvasapi import Canvas

from logger import LoggerFactory

_log = LoggerFactory.get_default_logger(__name__)
_log.setLevel(config.Canvas.LOG_LEVEL)

canvas = Canvas(
    base_url=config.Canvas.CANVAS_URL,
    access_token=config.Canvas.CANVAS_TOKEN
)
