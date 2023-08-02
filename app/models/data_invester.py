# models/data_item.py
from pydantic import BaseModel

class Invester(BaseModel):
    app_id:str
    app_secret:str
    broker_id:str
    app_code:str
    is_auto_queue:bool