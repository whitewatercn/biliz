import asyncio
import inspect
from functools import wraps
from typing import Callable, Union, Tuple
from urllib.parse import urlsplit

from biliz.exception import HandleError
from biliz.log import logger


def kwargs_filter(obj: Union[type, Callable], kwargs: dict):
    """

    :param obj:
    :param kwargs:
    :return:
    """
    sig = inspect.signature(obj)
    obj_require = set(sig.parameters.keys())

    def check(k):
        if k in obj_require:
            p = sig.parameters[k]
            # check type hint
            try:
                if p.annotation is inspect.Signature.empty or \
                        isinstance(kwargs[k], p.annotation):
                    return True
                else:
                    logger.debug(f"kwarg {k}:{kwargs[k]} has been drop due to type hint missmatch")
                    return False
            except TypeError:  # https://peps.python.org/pep-0604/#isinstance-and-issubclass
                # lower than 3.10, Union
                # TypeError: Subscripted generics cannot be used with class and instance checks
                return True
        return False

    kwargs = {k: kwargs[k] for k in filter(check, kwargs)}
    return kwargs


def auto_assemble(handle_func):
    @wraps(handle_func)
    def wrapped(cls, method: str, keys: Tuple[str, ...], options: dict):
        res = handle_func(cls, method, keys, options)
        if res is NotImplemented or res is None:
            return res
        executor, cor = res
        # handle func return class instead of instance
        if inspect.isclass(executor):
            kwargs = kwargs_filter(executor, options)
            executor = executor(**kwargs)
            logger.debug(f"auto assemble {executor} by {kwargs}")
        # handle func return async function instead of coroutine
        if inspect.iscoroutinefunction(cor):
            kwargs = kwargs_filter(cor, options)
            cors = []
            for key in keys:
                if not hasattr(cor, '__self__'):  # coroutine function has not bound to instance
                    cors.append(cor(executor, key, **kwargs))  # bound executor to self
                else:
                    cors.append(cor(key, **kwargs))
                logger.debug(f"auto assemble {cor} by {kwargs}")
            cor = asyncio.gather(*cors)
        return executor, cor

    return wrapped


def assign(cli_kwargs):
    from biliz.sites.bilibili import DownloaderBilibili, InformerBilibili

    method = cli_kwargs.pop('method')
    keys = cli_kwargs.pop('keys')
    if method not in {'cate', 'get_cate'}:
        numeric_methods = {'up', 'get_up', 'fav', 'get_favour'}
        for key in keys:
            try:
                url = urlsplit(key)
                host = url.hostname or ''
            except ValueError:
                host = ''
            if host and url.scheme in {'http', 'https'} and (
                    host in {'bilibili.com', 'b23.tv'} or host.endswith(('.bilibili.com', '.b23.tv'))):
                continue
            if method in numeric_methods and key.isascii() and key.isdecimal():
                continue
            raise HandleError('biliz 仅支持哔哩哔哩链接（bilibili.com 或 b23.tv）')

    handler = InformerBilibili if method == 'info' else DownloaderBilibili
    result = handler.handle(method, keys, cli_kwargs)
    if result is None:
        raise HandleError(f'哔哩哔哩下载器不支持命令：{method}')
    return result
