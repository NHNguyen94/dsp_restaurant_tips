from pydantic import BaseModel


class PredictionRequest(BaseModel):
    order_id: int
    date: str
    item_name: str
    item_type: str
    item_price: float
    transaction_type: str
    received_by: str
    time_of_sale: str
