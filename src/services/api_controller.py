import http.client
import json
<<<<<<< HEAD
import logging
=======
>>>>>>> main
import mimetypes
import os
import uuid
from io import BytesIO
from typing import Dict, List

import dotenv
import httpx
import requests

dotenv.load_dotenv()


class ApiController:
    def __init__(self):
        self.url = os.getenv("API_URL")

<<<<<<< HEAD
    def predict_with_file_manual_request(self, file_path: str) -> List[Dict]:
        host = "127.0.0.1:8000"
        url = "/v1/prediction/predict"
=======
    def predict_with_file_manual_request(self, file_path: str, prediction_source: str) -> List[Dict]:
        host = "127.0.0.1:8000"
        # url = "/v1/prediction/predict"
        url = f"/v1/prediction/predict?prediction_source={prediction_source}"
>>>>>>> main

        boundary = str(uuid.uuid4())
        body = BytesIO()

        content_type, _ = mimetypes.guess_type(file_path)
        if content_type is None:
            content_type = "application/octet-stream"

        with open(file_path, "rb") as file:
            file_data = file.read()
            body.write(f"--{boundary}\r\n".encode())
            body.write(
                f'Content-Disposition: form-data; name="input_file"; filename="{os.path.basename(file_path)}"\r\n'.encode()
            )
            body.write(f"Content-Type: {content_type}\r\n\r\n".encode())
            body.write(file_data)
            body.write(b"\r\n")

        body.write(f"--{boundary}--\r\n".encode())

        headers = {
            "Accept": "application/json",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body.getvalue())),
        }

        connection = http.client.HTTPConnection(host)
        connection.request("POST", url, body.getvalue(), headers)

        response = connection.getresponse()
        if response.status != 200:
            raise Exception(f"Failed to make prediction: {response.reason}")

        response_data = response.read().decode()
        return json.loads(response_data)

    def predict_with_file(self, file_path: str) -> List[Dict]:
        with open(file_path, "rb") as file:
            files = {"input_file": (file_path, file, "text/csv")}
            response = requests.post(
                f"{self.url}/prediction/predict", files=files, timeout=10
            )
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
