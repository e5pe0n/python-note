from typing import Callable, Any, ParamSpecArgs, ParamSpecKwargs
from datetime import datetime


def fmt_f_call(f: Callable, *args, **kwargs) -> str:
    args_s = ", ".join([str(arg) for arg in args])
    kwargs_s = ", ".join([f"{k}={v}" for k, v in kwargs.items()])

    return f"{f.__name__}({args_s if args else ''}"\
        f"{', ' if (args and kwargs) else '' }{kwargs_s if kwargs else ''})"


def fmt_f_return(f: Callable, return_value: Any, *args, **kwargs) -> str:
    return f"{fmt_f_call(f, *args, **kwargs)} returned `{return_value}`"


def fmt_f_call_with_dt(f: Callable, *args, **kwargs) -> str:
    return f"{datetime.now()} | {fmt_f_call(f, *args, **kwargs)}"


def fmt_f_return_with_dt(
    f: Callable, return_value: Any,
    *args,
    **kwargs,
) -> str:
    return f"{datetime.now()} |"\
        f" {fmt_f_return(f, return_value, *args, **kwargs)}"


def trace(
    f_call_fmter: Callable[[Callable, ParamSpecArgs, ParamSpecKwargs], str],
    f_return_fmter:
        Callable[[Callable, Any, ParamSpecArgs, ParamSpecKwargs], str],
) -> Callable:
    """Modify the given function `f`
    to print some information on the function
    before calling and after returned.

    Args:
        f_call_fmter
        (Callable[[Callable, ParamSpecArgs, ParamSpecKwargs], str]):
        a function to format information printed before function calling.
        the function should take `*args` and `*kwargs` and return a string.

        f_return_fmter
        (Callable[[Callable, Any, ParamSpecArgs, ParamSpecKwargs], str]):
        a function to format information printed after function returned.
        the function should take the return value, `*args` and `**kwargs`
        and return a string.

    Returns:
        Callable: a modified function
    """
    def wrapper(f: Callable) -> Callable:
        def _wrapper(*args, **kwargs) -> Any:
            print(f_call_fmter(f, *args, **kwargs))

            res = f(*args, **kwargs)

            print(f_return_fmter(f, res, *args, **kwargs))

            return res
        return _wrapper
    return wrapper


@trace(fmt_f_call, fmt_f_return)
def one() -> int:
    return 1


@trace(fmt_f_call_with_dt, fmt_f_return_with_dt)
def eq_name(name1: str, name2: str, case_sensitive: bool = True) -> bool:
    if case_sensitive:
        return name1 == name2

    return name1.lower() == name2.lower()


one()
# one()
# one() returned `1`

eq_name("alice", "Alice", case_sensitive=False)
# 2023-02-02 01:15:59.180540 | eq_name(alice, Alice, case_sensitive=False)
# 2023-02-02 01:15:59.180592 | eq_name(alice, Alice, case_sensitive=False) returned `True` # noqa: E501
