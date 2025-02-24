import pytest

from src.services.api_controller import ApiController


class TestApiController:
    test_file = "tests/resources/test_tips.csv"

    def test_predict_with_file(self):
        api_controller = ApiController()
        response = api_controller.predict_with_file(self.test_file)
        assert len(response) > 0

    @pytest.mark.asyncio
    async def test_async_predict_with_file(self):
        api_controller = ApiController()
        response = await api_controller.async_predict_with_file(self.test_file)
        assert len(response) > 0
