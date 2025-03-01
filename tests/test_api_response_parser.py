from src.utils.api_response_parser import ApiResponseParser


class TestApiResponseParser:
    def test_parse_response(self):
        test_data = [
            {
                "total_bill": 16.99,
                "sex": "Female",
                "smoker": False,
                "day": "Sun",
                "time": "Dinner",
                "size": 2,
                "tip": 1.13,
            },
            {
                "total_bill": 10.34,
                "sex": "Male",
                "smoker": False,
                "day": "Sun",
                "time": "Dinner",
                "size": 3,
                "tip": 1.68,
            },
            {
                "total_bill": 21.01,
                "sex": "Male",
                "smoker": False,
                "day": "Sun",
                "time": "Dinner",
                "size": 3,
                "tip": 3.36,
            },
        ]
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        response = ApiResponseParser.parse_response(test_data)
=======
        response = ApiResponseParser.parse_response(test_data, prediction_source="test")
>>>>>>> main
=======
        response = ApiResponseParser.parse_response(test_data, prediction_source="test")
>>>>>>> main
=======
        response = ApiResponseParser.parse_response(test_data, prediction_source="test")
>>>>>>> main
        assert len(response) == 3
        assert response[0].total_bill == 16.99
        assert response[1].day == "Sun"
        assert response[2].size == 3
