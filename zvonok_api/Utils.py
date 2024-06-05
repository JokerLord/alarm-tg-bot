import requests
import logging
from functools import wraps

logger = logging.getLogger(__name__)


class ZvonokApiException(Exception):
    pass


def check_request(request_func):
    """
    Decorator for status checking of API response
    """

    @wraps(request_func)
    def _wrapper(*args, **kwargs):
        resp: requests.Response = request_func(*args, **kwargs)
        if resp.status_code >= 400:
            raise ZvonokApiException(
                f"Api method with url = {resp.url} responded with code = {resp.status_code}"
            )
        try:
            resp_data = resp.json()
        except Exception:
            raise ZvonokApiException(f"Failed to parse json from Zvonok api response")
        if resp_data.get("status") == "error":
            raise ZvonokApiException(f"Zvonok api responded with error = {resp_data}")

        return resp_data

    return _wrapper
