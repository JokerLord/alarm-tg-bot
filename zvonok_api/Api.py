import requests
from requests.adapters import HTTPAdapter, Retry

from zvonok_api.Utils import check_request


class ZvonokManager:
    def __init__(
            self,
            public_api_key: str,
            campaign_id: str,
            api_host: str,
            n_retries: int = 3,
            backoff_factor: float = 0.1,
            debug: bool = False
    ) -> None:
        self.__public_api_key = public_api_key
        self.__campaign_id = campaign_id
        self.__api_host = api_host
        if self.__public_api_key is None:
            raise RuntimeError("Set ZVONOK_API_TOKEN env. variable")
        
        retries = Retry(
            total=n_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[408, 425, 429, 500, 502, 503, 504]
        )
        self.__requests_session = requests.Session()
        self.__requests_session.mount("https://", HTTPAdapter(max_retries=retries))

        self.__debug = debug

        self.__api_urls = {
            "create_call": "/manager/cabapi_external/api/v1/phones/call",
            "delete_call": "/manager/cabapi_external/api/v1/phones/remove_call",
            "check_call_by_phone": "/manager/cabapi_external/api/v1/phones/call_by_id"
        }

    @check_request
    def create_call(self, phone: str) -> requests.Response:
        payload = {
            "public_key": self.__public_api_key,
            "phone": phone,
            "campaign_id": self.__campaign_id
        }
        response = self.__requests_session.post(self.__api_host + self.__api_urls["create_call"], data=payload)
        return response
    
    @check_request
    def delete_call(self, phone: str) -> requests.Response:
        payload = {
            "public_key": self.__public_api_key,
            "phone": phone,
            "campaign_id": self.__campaign_id
        }
        response = self.__requests_session.post(self.__api_host + self.__api_urls["delete_call"], data=payload)
        return response
    
    @check_request
    def check_call(self, phone: str) -> requests.Response:
        payload = {
            "public_key": self.__public_api_key,
            "phone": phone,
            "campaign_id": self.__campaign_id
        }
        response = self.__requests_session.post(self.__api_host + self.__api_urls["check_call_by_phone"], data=payload)
        return response
