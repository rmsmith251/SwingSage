import logging
from functools import lru_cache


@lru_cache()
def get_logger(log_level: str) -> logging.Logger:
    """
    Source: https://github.com/tiangolo/fastapi/issues/1508#issuecomment-638365277
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % log_level)

    logger = logging.getLogger("uvicorn.access")
    logger.setLevel(numeric_level)

    return logger
