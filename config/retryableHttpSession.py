from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import requests
import config.loggerFactory as loggerFactory
import logging

logger = loggerFactory.get_logger(__name__, logging.DEBUG)

class LoggingRetry(Retry):
    def increment(self, method=None, url=None, response=None, error=None, _pool=None, _stacktrace=None):
        new_retry = super().increment(method=method, url=url, response=response, error=error, _pool=_pool, _stacktrace=_stacktrace)

        status = getattr(response, "status", None) or (response.status if response is not None and hasattr(response, "status") else None)
        err_msg = repr(error) if error is not None else None
        logger.debug(f"Retrying request. status={status} method={method} url={url} error={err_msg}")

        return new_retry

def create_retryable_session() -> requests.Session:
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=LoggingRetry(
        total=3,
        backoff_factor=1,
        status_forcelist=[404, 500, 502, 503, 504],
    ))
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session