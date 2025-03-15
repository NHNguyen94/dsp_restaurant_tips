# import pytest
#
# from src.services.api_controller import ApiController
#
# # This will write into database, so only enable when needed
# class TestApiController:
#     api_controller = ApiController()
#     test_file = "tests/resources/test_tips.csv"
#
#     def test_predict_with_file(self):
#         response = self.api_controller.predict_with_file(self.test_file)
#         assert len(response) > 0
#
#     def test_predict_with_file_manual_request(self):
#         response = self.api_controller.predict_with_file_manual_request(self.test_file, "scheduled_predictions")
#         print(f"\nresponse from manual request: {response}")
#         assert len(response) > 0
#
#     @pytest.mark.asyncio
#     async def test_async_predict_with_file(self):
#         response = await self.api_controller.async_predict_with_file(self.test_file)
#         assert len(response) > 0
