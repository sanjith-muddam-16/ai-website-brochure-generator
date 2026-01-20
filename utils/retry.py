import time
from typing import Callable, TypeVar

T = TypeVar("T")


def retry(
    fn: Callable[[], T],
    retries: int = 3,
    backoff: float = 1.0,
    exceptions: tuple = (Exception,),
) -> T:
    last_exception = None

    for attempt in range(retries):
        try:
            return fn()
        except exceptions as e:
            last_exception = e
            time.sleep(backoff * (2 ** attempt))

    raise last_exception
