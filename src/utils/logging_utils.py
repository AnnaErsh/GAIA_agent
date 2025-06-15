import threading
import logging
from typing import Any

# Thread-local storage for indentation level
_indent = threading.local()
_indent.level = 0


class IndentFormatter(logging.Formatter):
    def format(self, record):
        level = getattr(_indent, "level", 0)
        indent_space = "  " * level  # Two spaces per level
        record.msg = f"{indent_space}{record.msg}"
        return super().format(record)


class Logger:
    _logger = None

    @classmethod
    def setup_logging(cls) -> None:
        if cls._logger is None:
            handler = logging.StreamHandler()
            formatter = IndentFormatter("[%(levelname)s][%(funcName)s] %(message)s")
            handler.setFormatter(formatter)
            cls._logger = logging.getLogger("Logger")
            cls._logger.addHandler(handler)
            cls._logger.setLevel(logging.INFO)

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls._logger is None:
            cls.setup_logging()
        return cls._logger


# Context manager for indenting
from contextlib import contextmanager


@contextmanager
def log_indent():
    _indent.level = getattr(_indent, "level", 0) + 1
    try:
        yield
    finally:
        _indent.level = max(_indent.level - 1, 0)
