import logging

from dq_sus.utils.logger import setup_logging
from typing import Optional

def test_setup_logging() -> None:
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logger = setup_logging()

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter: Optional[logging.Formatter] = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)
    assert isinstance(logger, logging.Logger)
    assert logger.name == "dq_sus.utils.logger"
    assert logger.level == logging.INFO
    assert len(logger.handlers) > 0

    handler = logger.handlers[0]
    assert isinstance(handler, logging.StreamHandler)
    formatter = handler.formatter
    assert formatter is not None
    assert formatter._fmt == "%(asctime)s - %(levelname)s - %(message)s"
