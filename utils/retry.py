import time
from typing import Callable, TypeVar
from openai import RateLimitError

T = TypeVar("T")

def retry(
    fn: Callable[[], T],
    retries: int = 3,
    backoff: float = 1.0,
) -> T:
    last_exception = None

    for attempt in range(retries):
        try:
            return fn()

        except RateLimitError as e:
            retry_after = getattr(e, "retry_after", None)
            sleep_time = retry_after if retry_after else backoff * (2 ** attempt)
            time.sleep(sleep_time)
            last_exception = e

        except Exception as e:
            time.sleep(backoff * (2 ** attempt))
            last_exception = e

    raise last_exception

