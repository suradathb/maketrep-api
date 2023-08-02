from fastapi import APIRouter,HTTPException,FastAPI
from settrade_v2 import MarketRep,Investor
from settrade_v2.errors import SettradeError
from typing import Optional
# from app.models.data_account import AccountInfo
# from app.models.data_order import Order,ItemOrderNo
from models.data_account import AccountInfo
from models.data_order import Order,ItemOrderNo
from decouple import config
import requests

router = APIRouter(
    prefix='/api/v1',
    tags=['Maketrep API DERIVATIVES'],
    responses={404:{
        'message':'Not found'
    }}
)

app_id = config("APP_ID")
app_secret = config("APP_SECRET")
app_code = config("APP_CODE")
broker_id = config("BROKER_ID")
is_auto_queue = config("IS_AUTO_QUEUE")

# maketrep  = MarketRep(
#                 app_id="rccmkjqLZSP8x5fN",                                 
#                 app_secret="AJX9QLmaBhdV4EYScOZTn9ZwC+ViVj67GJSoEQtkHR9v", 
#                 broker_id="SANDBOX",
#                 app_code="SANDBOX",
#                 is_auto_queue = False)

# investor = Investor(
#                 app_id="rM4oHZAjXc6KxREy",                                 
#                 app_secret="AJ0+ob6EZ+Ww5Ih2CupVV7QxZOBhBWKKiTSrekwgblfR", 
#                 broker_id="SANDBOX",
#                 app_code="SANDBOX",
#                 is_auto_queue = False)

investor = Investor(
                app_id=app_id,                                 
                app_secret=app_secret, 
                broker_id=broker_id,
                app_code=app_code,
                is_auto_queue = is_auto_queue)

# Get Account Info ดึงข้อมูล account information start 
@router.get("/accountinfo")
def Account_Info(account:str):
    try:
        deri = investor.Derivatives(account_no=account)
        account_info_dict = deri.get_account_info()
        account_info = AccountInfo(**account_info_dict)
        if(account_info):
            return account_info 
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args )
# Get Account Info ดึงข้อมูล account information End
     
#  Get Order ดึงข้อมูล order โดยระบุ order number จาก derivatives object start
@router.get("/order")
def Get_Order(order:int,account:str):
    try:
        deri = investor.Derivatives(account_no=account)
        order_info_dist = deri.get_order(order_no=order)
        if(order_info_dist):
            return order_info_dist
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args ) 
#  Get Order ดึงข้อมูล order โดยระบุ order number จาก derivatives object End

# Get Orders ดึงข้อมูล order ทั้งหมด Start
@router.get("/orders") 
def  Get_Orders(account:str):
    try:
        deri = investor.Derivatives(account_no=account)
        orders = deri.get_orders()
        if(orders):
            return orders
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args ) 
# Get Orders ดึงข้อมูล order ทั้งหมด End
 
# Get Orders By Account Number ดึงข้อมูล order ทั้งหมดจาก derivatives object เฉพาะของ account number Start
@router.get("/ordersby") 
def  Get_Orders_By_Account_Number(account:str,account_no:str):
    try:
        deri = investor.Derivatives(account_no=account)
        order_list  = deri.get_orders_by_account_no(account_no=account_no)
        if(order_list):
            return order_list
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args ) 
# Get Orders By Account Number ดึงข้อมูล order ทั้งหมดจาก derivatives object เฉพาะของ account number End


# Get Portfolios ดึงข้อมูล portfolio (สัญญาที่เปิดอยู่) จาก derivatives object Start
@router.get("/portfolios") 
def  Get_Portfolios(account:str):
    try:
        deri = investor.Derivatives(account_no=account)
        portfolios = deri.get_portfolios()
        if(portfolios):
            return portfolios
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args )
# Get Portfolios ดึงข้อมูล portfolio (สัญญาที่เปิดอยู่) จาก derivatives object End

# Get Trades ดึงข้อมูล trade ทั้งหมด จาก derivatives object Start
@router.get("/trades") 
def  Get_Trades(account:str):
    try:
        deri = investor.Derivatives(account_no=account)
        trade_list = deri.get_trades()
        if(trade_list):
            return trade_list
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args )
# Get Trades ดึงข้อมูล trade ทั้งหมด จาก derivatives object End

# Place Order ส่ง/วาง order จากนั้นจะได้ order object กลับมา Start
@router.post("/order") 
# def Place_Order(account:str,account_no:str, symbol:str, side:str, position:str, price_type:str, price:float, volume:int, validity_type:str, iceberg_vol:int, validity_date_condition:str|None == None, stop_condition:str, stop_symbol:str, stop_price:float, trigger_session:str, bypass_warning:bool):
def Place_Order(account:str):
    try:
        deri = investor.Derivatives(account_no=account)
        # doc_side = side
        # positions = position
        # price_types = price_type
        # validity_types = validity_type
        # if doc_side == "Long":
        #     doc_side = "Long"
        # elif doc_side == "Short":
        #     doc_side = "Short"
        # else:
        #     return {"msg": "Error side values Possible values are Long And Short"}
        
        # if positions == "Open":
        #     positions = "Open"
        # elif positions == "Close":
        #     positions = "Close"
        # elif positions == "Auto":
        #     positions = "Auto"
        # else:
        #     return {"msg": "Error Position values Possible values are Open,Close and Auto"}
        
        # if price_types == "Limit":
        #     price_types = "Limit"
        # elif price_types == "ATO":
        #     price_types = "ATO"
        # elif price_types == "MP-MTL":
        #     price_types = "MP-MTL"
        # elif price_types == "MP-MKT":
        #     price_types = "MP-MKT"
        # else:
        #     return {"msg":" Error price_type values Possible values are Limit,ATO,MP-MTL and MP-MKT"}
        
        # if validity_types == "Day":
        #     validity_types = "Day"
        # elif validity_types == "FOK":
        #     validity_types = "FOK"
        # elif validity_types == "IOC":
        #     validity_types = "IOC"
        # elif validity_types == "Date":
        #     validity_types = "Date"
        # elif validity_types == "Cancel":
        #     validity_types = "Cancel"
        # else:
        #     return {"msg": "Error price_type values Possible values are Day,FOK,IOC,Date and Cancel"}
        
        order = deri.place_order(
                    symbol="GDU23",
                    price=1995.1,
                    volume=13,
                    side="Short",
                    position="Auto",
                    pin="000000",
                    price_type="Limit",
                    validity_type="Day")
        if(order):
            return order
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args ) 
# Place Order ส่ง/วาง order จากนั้นจะได้ order object กลับมา End

# Change Order  เปลี่ยนข้อมูล order ที่ส่งไปจาก place order Start
@router.put('/changorder')
def Chang_Order(account:str,pin:str,order_no:int, new_price:Optional[float]|None = None, new_volume:Optional[int] |None = None, bypass_warning:Optional[bool] |None = None):
    try:
        deri = investor.Derivatives(account_no=account)
        chang_order = deri.change_order(
            pin=pin,
            order_no=order_no,
            new_price=new_price,
            new_volume=new_volume,
            bypass_warning=bypass_warning,
            )
        return chang_order
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args )
# Change Order  เปลี่ยนข้อมูล order ที่ส่งไปจาก place order End

# Cancel Order ยกเลิก order Start
@router.put('/cancelorder')
async def Cancel_Order(account: str,order:int,pin:str):
      try:
        deri = investor.Derivatives(account_no=account)
        cancel_order = deri.cancel_order(order_no=order, pin=pin)
        return {"msg":f"Cancel Order No {order} Success. And Doc Return Empty dictionary."}
      except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args )
# Cancel Order ยกเลิก order End    

# Cancel Orders ยกเลิก order มากกว่า 1 order Start
@router.put('/cancelorders')
async def Cancel_Orders(account: str,pin:str,orders_no:list[int]):
      try:
        deri = investor.Derivatives(account_no=account)
        cancel_orders = deri.cancel_orders(order_no_list=orders_no, pin=pin)
        if(cancel_orders):
            return cancel_orders
      except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail=e.args )
# Cancel Orders ยกเลิก order มากกว่า 1 order End

# Place Trade Report ส่ง place trade report Start
@router.get("/placetradereport") 
def  Place_Trade_Report(symbol:str, position:str, price:float, volume:int, cpm:str, tr_type:str, buyer:Optional[str]|None=None, seller:Optional[str] |None = None, control_key:Optional[str]|None = None):
    try:
        deri = investor.Derivatives()
        place_trade_report = deri.place_trade_report(
            buyer=buyer,
            seller= seller,
            symbol= symbol,
            position= position,
            price= price,
            volume= volume,
            cpm= cpm,
            tr_type= tr_type,
            control_key= control_key
        )
        if(place_trade_report):
            return place_trade_report
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args )
# Place Trade Report ส่ง place trade report End