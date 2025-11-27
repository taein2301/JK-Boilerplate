import sys

from loguru import logger

from app.utils.config import config


def setup_logger():
    """Configure the logger based on app settings."""
    logger.remove()  # Remove default handler

    # Console handler
    logger.add(
        sys.stderr,
        level=config.log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
    )

    # File handler (optional, example)
    # logger.add("logs/app.log", rotation="500 MB", level=config.log_level)

    return logger


def configure_file_logging(app_name: str):
    """Add a file handler with daily rotation."""
    import os

    home_dir = os.path.expanduser("~")
    log_file = f"{home_dir}/logs/{app_name}_{{time:YYYYMMDD}}.log"
    logger.add(
        log_file,
        rotation="00:00",  # Rotate daily at midnight
        retention="30 days",  # Keep logs for 30 days
        level=config.log_level,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level: <8} | "
            "{name}:{function}:{line} - "
            "{message}"
        ),
    )


# Initialize logger with default console handler
setup_logger()
