import os
from typing import Dict, List

import dotenv
import httpx
import requests

dotenv.load_dotenv()


class ApiController:
    def __init__(self):
        self.url = os.getenv("API_URL")

    def predict_with_file(self, file_path: str) -> List[Dict]:
        with open(file_path, "rb") as file:
            files = {"input_file": file}
            response = requests.post(f"{self.url}/prediction/predict", files=files)
        if response.status_code != 200:
            raise Exception(f"Failed to make prediction: {response.text}")
        return response.json()

    async def async_predict_with_file(self, file_path: str) -> List[Dict]:
        async with httpx.AsyncClient() as client:
            with open(file_path, "rb") as file:
                files = {"input_file": file}
                response = await client.post(
                    f"{self.url}/prediction/predict", files=files
                )

        if response.status_code != 200:
            raise Exception(f"Failed to make prediction: {response.text}")

        return response.json()
