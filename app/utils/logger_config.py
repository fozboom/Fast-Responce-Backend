import logging


def get_logger(
    module_name: str,
) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s: %(message)s",
    )
    return logging.getLogger(module_name)
