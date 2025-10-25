import logging
import os
import json
from datetime import datetime

import logging.handlers

_loggers = {}


_DEFAULT_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_DEFAULT_TIMEFMT = "%H:%M:%S"


def get_logger(
    name: str = None,
    level: int | str = logging.INFO,
    log_to_console: bool = True,
    log_to_file: bool = False,
    file_path: str | None = None,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    formatter: logging.Formatter | None = None,
    disable_propagation: bool = True
) -> logging.Logger:

    if name is None:
        name = "root"

    # map string level names to constants
    if isinstance(level, str):
        level = logging.getLevelName(level.upper())

    if name in _loggers:
        logger = _loggers[name]
        logger.setLevel(level)
        logger.propagate = not disable_propagation
        return logger

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = not disable_propagation

    # choose formatter
    if formatter is None:
        formatter_instance = logging.Formatter(_DEFAULT_FORMAT, datefmt=_DEFAULT_TIMEFMT)
    else:
        formatter_instance = formatter

    if log_to_console:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter_instance)
        logger.addHandler(ch)

    if log_to_file:
        if not file_path:
            logs_dir = "logs"
            os.makedirs(logs_dir, exist_ok=True)
            file_name = f"{name}.log" if name != "root" else "application.log"
            file_path = os.path.join(logs_dir, file_name)
        else:
            os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)

        fh = logging.handlers.RotatingFileHandler(
            filename=file_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        fh.setLevel(level)
        fh.setFormatter(formatter_instance)
        logger.addHandler(fh)

    _loggers[name] = logger
    return logger
