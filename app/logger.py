from pathlib import Path
from app.customize_logger import CustomizeLogger

config_path = Path("app/logging_config.json")

logger = CustomizeLogger.make_logger(config_path)
