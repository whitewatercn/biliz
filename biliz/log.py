import logging
from rich.logging import RichHandler


def get_logger():
    biliz_logger = logging.getLogger("biliz")
    # 如果logger已经配置过handler，直接返回logger实例
    if biliz_logger.hasHandlers():
        return biliz_logger
    biliz_logger.setLevel(logging.INFO)
    # 创建自定义的RichHandler
    custom_rich_handler = RichHandler(
        show_time=False,
        show_path=False,
        markup=True,
        keywords=RichHandler.KEYWORDS + ['STREAM'],
        rich_tracebacks=True
    )
    # 设置日志格式
    formatter = logging.Formatter("{message}", style="{", datefmt="[%X]")
    custom_rich_handler.setFormatter(formatter)
    # 为logger添加自定义的RichHandler
    biliz_logger.addHandler(custom_rich_handler)
    return biliz_logger


logger = get_logger()
