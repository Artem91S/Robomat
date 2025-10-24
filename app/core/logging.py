import sys

from loguru import logger

logger.remove()

SCREEN_FORMAT = (
    "<cyan>>>></cyan> {time:YYYY-MM-DD HH:mm:ss} | "
    "<level><bold>{level}</bold></level> | "
    "<cyan>Path</cyan>: {name} -> <cyan>Func</cyan>: {function} -> <cyan>Line</cyan>: {line} | "
    "<level>{message}</level>\n"
)


def logger_format(record):
    if record['level'].name == 'ERROR':
        return SCREEN_FORMAT + "\n<level>{exception}</level>\n"
    return SCREEN_FORMAT


logger.add(
    sink=sys.stdout,
    format=logger_format,
    colorize=True
)
