# models/data_item.py
from pydantic import BaseModel
from datetime import date,datetime ,time ,timedelta
from typing import Optional

class Order(BaseModel):
    accountNo: str
    balanceQty: int
    canCancel: bool
    canChange: bool
    cancelId: Optional[str] = "None"
    cancelQty:int
    cancelTime: datetime
    cpm: Optional[str] = "None"
    entryId: str
    entryTime: datetime
    icebergVol: int
    isStopOrderNotActivate: str
    matchQty: int
    orderNo: int
    position: str
    price: float
    priceDigit:int
    priceType: str
    qty:int
    rejectCode: int
    rejectReason: Optional[str] = "None"
    showStatus: str
    side: str
    status: str
    statusMeaning: str
    symbol: str
    terminalType: str
    tfxOrderNo: str
    trType: Optional[str] = "None"
    tradeDate: date
    transactionTime: datetime
    triggerCondition: Optional[str] = "None"
    triggerPrice: int
    triggerSession: Optional[str] = "None"
    triggerSymbol: Optional[str] = "None"
    validToDate: Optional[str] = "None"
    validity: str
    version: int

class ItemOrderNo(BaseModel):
    orders_no:list[int]

class OrderRequest(BaseModel):
    account_no:str
    symbol: str = None
    side: str = None
    position: str = None
    price_type: str =   None
    price: float = 0.0
    volume: int = 0
    validity_type: str = None
    iceberg_vol: int = 0
    validity_date_condition: Optional[str] = None
    stop_condition: Optional[str] = None
    stop_symbol: Optional[str] = None
    stop_price: Optional[float] = None
    trigger_session: Optional[str] = None
    bypass_warning: bool

class ChangOrder(BaseModel):
    account_no:str
    order_no:int
    new_price:Optional[float] = None
    new_volume:Optional[int] = None
    bypass_warning:Optional[bool] = None
    new_account_no:Optional[str] = None

class PlaceTradeReport(BaseModel):
    symbol: str
    position: str
    price: float
    volume: int
    cpm: str
    tr_type: str
    buyer: Optional[str] = None
    seller: Optional[str] = None
    control_key: Optional[str] = None
