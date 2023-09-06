from fastapi import APIRouter,HTTPException,FastAPI,Depends
from settrade_v2 import MarketRep,Investor
from settrade_v2.errors import SettradeError
from typing import Optional
from datetime import datetime
# from app.models.data_account import AccountInfo
# from app.models.data_order import Order,ItemOrderNo,OrderRequest,ChangOrder,PlaceTradeReport
from models.data_account import AccountInfo
from models.data_order import Order,ItemOrderNo,OrderRequest,ChangOrder,PlaceTradeReport
import requests

router = APIRouter(
    prefix='/api/kss/v3',
    tags=['DERIVATIVES OMS API KSS'],
    responses={404:{
        'message':'Not found'
    }}
)

app_id = None
app_secret = None
broker_id = "SANDBOX"
app_code = "SANDBOX"
is_auto_queue=False

# Function to change app_id and app_secret
def change_credentials(new_app_id, new_app_secret):
    global app_id, app_secret
    app_id = new_app_id
    app_secret = new_app_secret

# Get Account Info ดึงข้อมูล account information start 
@router.get('/app_ID/{app_id_param}/secret/{app_secret_param}/account/{account}')
def accountinfo(account: str, app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    global app_id, app_secret

    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)

    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")

    # Your logic for using app_id and app_secret here
    try:
        investor = Investor(app_id=app_id, app_secret=app_secret, broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = investor.Derivatives(account_no=account)
        account_info_dict = deri.get_account_info()
        account_info = AccountInfo(**account_info_dict)
        if account_info:
            return account_info
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code, detail=e.args)
# Get Account Info ดึงข้อมูล account information End
     
#  Get Order ดึงข้อมูล order โดยระบุ order number จาก derivatives object start
@router.get("/app_ID/{app_id_param}/secret/{app_secret_param}/account/{account}/order/{order}")
def Get_Order_Investor(order:int,account:str,app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)
        
    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        investor = Investor(app_id=app_id, app_secret=app_secret, broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = investor.Derivatives(account_no=account)
        order_info_dist = deri.get_order(order_no=order)
        if(order_info_dist):
            return order_info_dist
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args ) 
#  Get Order ดึงข้อมูล order โดยระบุ order number จาก derivatives object End

# Get Portfolios ดึงข้อมูล portfolio (สัญญาที่เปิดอยู่) จาก derivatives object Start
@router.get("/app_ID/{app_id_param}/secret/{app_secret_param}/portfolios/{account}") 
def  Get_Portfolios(account:str,app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)
        
    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        investor = Investor(app_id=app_id, app_secret=app_secret, broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = investor.Derivatives(account_no=account)
        portfolios = deri.get_portfolios()
        if(portfolios):
            return portfolios
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args )
# Get Portfolios ดึงข้อมูล portfolio (สัญญาที่เปิดอยู่) จาก derivatives object End


# Get Order ดึงข้อมูล order ตาม orderNo Start
@router.get("/app_ID/{app_id_param}/secret/{app_secret_param}/account/{account}/orderNo/{order_no}") 
def Get_Order(account:str,order_no:int,app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)
        
    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        investor = Investor(app_id=app_id, app_secret=app_secret, broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = investor.Derivatives(account_no=account)
        order = deri.get_order(order_no=order_no)
        if(order):
            return order
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args ) 
# Get Order ดึงข้อมูล order ตาม orderNo End

# Get Orders ดึงข้อมูล order ทั้งหมด Start
@router.get("/app_ID/{app_id_param}/secret/{app_secret_param}/account/{account}") 
def  Get_Orders(account:str,app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)
        
    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        investor = Investor(app_id=app_id, app_secret=app_secret, broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = investor.Derivatives(account_no=account)
        orders = deri.get_orders()
        if(orders):
            return orders
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args ) 
# Get Orders ดึงข้อมูล order ทั้งหมด End
 
# Get Orders By Account Number ดึงข้อมูล order ทั้งหมดจาก derivatives object เฉพาะของ account number Start
@router.get("/app_ID/{app_id_param}/secret/{app_secret_param}/account_No/{account}") 
def  Get_Orders_By_Account_Number(account:str,app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)
        
    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        investor = Investor(app_id=app_id, app_secret=app_secret, broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = investor.Derivatives(account_no=account)
        order_list  = deri.get_orders_by_account_no(account_no=account)
        if(order_list):
            return order_list
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args ) 
# Get Orders By Account Number ดึงข้อมูล order ทั้งหมดจาก derivatives object เฉพาะของ account number End

# Get Trades ดึงข้อมูล trade ทั้งหมด จาก derivatives object Start
@router.get("/app_ID/{app_id_param}/secret/{app_secret_param}/trades/{account}") 
def  Get_Trades(account:str,app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)
        
    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        investor = Investor(app_id=app_id, app_secret=app_secret, broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
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
def Place_Order(account:str,data:OrderRequest,app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)
        
    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        investor = Investor(app_id=app_id, app_secret=app_secret, broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
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
                    symbol=data.symbol,
                    price=data.price,
                    volume=data.volume,
                    side=data.side,
                    position=data.position,
                    pin=data.pin,
                    price_type=data.price_type,
                    validity_type=data.validity_type)
        if(order):
            return order
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args ) 
# Place Order ส่ง/วาง order จากนั้นจะได้ order object กลับมา End

# Change Order  เปลี่ยนข้อมูล order ที่ส่งไปจาก place order Start
@router.put('/changorder')
def Chang_Order(account:str,body:ChangOrder,app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)
        
    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        investor = Investor(app_id=app_id, app_secret=app_secret, broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = investor.Derivatives(account_no=account)
        chang_order = deri.change_order(
            account_no=account,
            order_no=body.order_no,
            new_price=body.new_price,
            new_volume=body.new_volume,
            bypass_warning=body.bypass_warning,
            )
        return chang_order
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args )
# Change Order  เปลี่ยนข้อมูล order ที่ส่งไปจาก place order End

# Cancel Order ยกเลิก order Start
@router.put('/cancelorder')
async def Cancel_Order(account: str,order:int,pin:str,app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
      # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)
        
    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        investor = Investor(app_id=app_id, app_secret=app_secret, broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = investor.Derivatives(account_no=account)
        cancel_order = deri.cancel_order(order_no=order, pin=pin)
        return {"msg":f"Cancel Order No {order} Success. And Doc Return Empty dictionary."}
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args )
# Cancel Order ยกเลิก order End    

# Cancel Orders ยกเลิก order มากกว่า 1 order Start
@router.put('/cancelorders')
async def Cancel_Orders(account: str,pin:str,orders_no:ItemOrderNo,app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)
        
    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        investor = Investor(app_id=app_id, app_secret=app_secret, broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = investor.Derivatives(account_no=account)
        cancel_orders = deri.cancel_orders(order_no_list=orders_no.orders_no, pin=pin)
        if(cancel_orders):
            return cancel_orders
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail=e.args )
# Cancel Orders ยกเลิก order มากกว่า 1 order End

# Place Trade Report ส่ง place trade report Start
@router.post("/report") 
def  Place_Trade_Report(account:str,report:PlaceTradeReport,app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)
        
    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        investor = MarketRep(app_id=app_id, app_secret=app_secret, broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = investor.Derivatives()
        place_trade_report = deri.place_trade_report(
            buyer=report.buyer,
            seller= report.seller,
            symbol= report.symbol,
            position= report.position,
            price= report.price,
            volume= report.volume,
            cpm= report.cpm,
            tr_type= report.tr_type,
            control_key= report.control_key
        )
        if(place_trade_report):
            return place_trade_report
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code,detail= e.args )
# Place Trade Report ส่ง place trade report End





    