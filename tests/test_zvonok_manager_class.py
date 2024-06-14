from unittest import TestCase
from unittest.mock import MagicMock, patch

from zvonok_api.Api import ZvonokManager
from configs import Config


class TestZvonokManagerClass(TestCase):

    def setUp(self):
        self.config = Config.TestConfig()
        self.zvonok_manager = ZvonokManager(
            public_api_key=self.config.ZVONOK_API_TOKEN,
            campaign_id=self.config.ZVONOK_CAMPAIGN_ID,
            api_host=self.config.ZVONOK_API_URI,
        )

    def test_zvonok_manager_create_call(self):
        session = MagicMock()
        response = MagicMock()
        response.status_code = 200
        session.post = MagicMock(return_value=response)
        with patch.object(self.zvonok_manager, "_ZvonokManager__requests_session", session):
            self.zvonok_manager.create_call("+11111111111")
            self.zvonok_manager._ZvonokManager__requests_session.post.assert_called_with(
                "http://127.0.0.1:8080/manager/cabapi_external/api/v1/phones/call/",
                data={
                    "public_key": self.config.ZVONOK_API_TOKEN,
                    "phone": "+11111111111",
                    "campaign_id": self.config.ZVONOK_CAMPAIGN_ID,
                }
            )

    def test_zvonok_manager_delete_call(self):
        session = MagicMock()
        response = MagicMock()
        response.status_code = 200
        session.post = MagicMock(return_value=response)
        with patch.object(self.zvonok_manager, "_ZvonokManager__requests_session", session):
            self.zvonok_manager.delete_call("+11111111111")
            self.zvonok_manager._ZvonokManager__requests_session.post.assert_called_with(
                "http://127.0.0.1:8080/manager/cabapi_external/api/v1/phones/remove_call/",
                data={
                    "public_key": self.config.ZVONOK_API_TOKEN,
                    "phone": "+11111111111",
                    "campaign_id": self.config.ZVONOK_CAMPAIGN_ID,
                }
            )

    def test_zvonok_manager_check_call(self):
        session = MagicMock()
        response = MagicMock()
        response.status_code = 200
        session.post = MagicMock(return_value=response)
        with patch.object(self.zvonok_manager, "_ZvonokManager__requests_session", session):
            self.zvonok_manager.check_call("+11111111111")
            self.zvonok_manager._ZvonokManager__requests_session.post.assert_called_with(
                "http://127.0.0.1:8080/manager/cabapi_external/api/v1/phones/call_by_id/",
                data={
                    "public_key": self.config.ZVONOK_API_TOKEN,
                    "phone": "+11111111111",
                    "campaign_id": self.config.ZVONOK_CAMPAIGN_ID,
                }
            )
