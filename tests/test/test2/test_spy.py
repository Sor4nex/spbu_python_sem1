import pytest
from src.test.test2.spy import *
import datetime


@logger("my_log.txt")
def f(a, b):
    if a != 0:
        return f(a - 1, b - 1)
    return b


@logger
def foo(a, b, **kwargs):
    return a, b


@logger
def foo2():
    return True


foo3 = lambda x: x


@logger
def foo4(x, **kwargs):
    return x


def test_logger(monkeypatch) -> None:
    @logger("my_log.txt")
    def f(a, b):
        if a != 0:
            return f(a - 1, b - 1)
        return b

    fake_time = datetime.datetime(2012, 12, 12, 2, 28, 00)
    monkeypatch.setattr(datetime, "datetime", fake_time)
    f(1, 1)
    f(b=2, a=1)
    f.output_file.close()
    result = open("my_log.txt", "r").read()
    assert result == (
        "01/12/2023 15:11:14 f a=0 b=0 0\n"
        "01/12/2023 15:11:14 f a=1 b=1 0\n"
        "01/12/2023 15:11:14 f a=0 b=1 1\n"
        "01/12/2023 15:11:14 f a=1 b=2 1\n"
    )
