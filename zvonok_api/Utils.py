import requests

class ZvonokApiException(Exception):
    pass

def check_request(request_func):
    """
    Decorator for status checking of API response
    """
    def _wrapper(*args, **kwargs):
        resp: requests.Response = request_func(*args, **kwargs)
        resp_data = resp.json()
        if resp_data.get("status") == "error":
            raise ZvonokApiException(
                f"API call with url {resp.url} replied with code {resp.status_code}"
                f" with response data = {resp_data.get('data')}"
            )
        return resp
    return _wrapper
