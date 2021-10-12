import config
from canvasapi import Canvas

from logger import LoggerFactory

_log = LoggerFactory.get_default_logger(__name__)
_log.setLevel(config.CanvasConfig.LOG_LEVEL)

canvas = Canvas(
    base_url=config.CanvasConfig.CANVAS_URL,
    access_token=config.CanvasConfig.CANVAS_TOKEN
)
