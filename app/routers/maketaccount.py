from fastapi import APIRouter, HTTPException, FastAPI, Depends, Body
from settrade_v2 import MarketRep
from settrade_v2.errors import SettradeError
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.data_account import AccountInfo
from app.models.data_order import Order,ItemOrderNo,OrderRequest,ChangOrder,PlaceTradeReport,PlasOrders
from app.routers.helpers import logger_in,logger_out,logger_error,logger_body,logger_Trade,logger_Trade_error,logger_in_Trade_report
# from models.data_account import AccountInfo
# from models.data_order import Order, ItemOrderNo, OrderRequest, ChangOrder, PlaceTradeReport, PlasOrders
# from routers.helpers import logger_in, logger_out, logger_error, logger_body, logger_Trade, logger_Trade_error, logger_in_Trade_report
import requests


router = APIRouter(
    prefix='/api/kss/v3',
    tags=['DERIVATIVES OMS API KSS'],
    responses={404: {
        'message': 'Not found'
    }}
)

fun = ''


app_id = None
app_secret = None
broker_id = "029"
app_code = "TRADEREPORT"
is_auto_queue = False


# Function to change app_id and app_secret
def change_credentials(new_app_id, new_app_secret):
    global app_id, app_secret
    app_id = new_app_id
    app_secret = new_app_secret
    print(app_id, app_secret)


# Get Account Info ดึงข้อมูล account information start
@router.get('/accountinfo/app_ID/{app_id_param}/secret/{app_secret_param}/account/{account}')
def accountinfo(account: str, ic_code: str, code_app: str, app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    try:
        # If app_id_param and app_secret_param are provided in the request, update the global values
        if app_id_param and app_secret_param:
            change_credentials(app_id_param, app_secret_param)
            # logger.info(f"Updated app_id and app_secret to {app_id_param}, {app_secret_param}")

        # Check if app_id and app_secret are available
        if not app_id or not app_secret:
            error_msg = "App credentials are not set. Please provide app_id and app_secret."
            # logger.error(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)

    # Your logic for using app_id and app_secret here
        fun = "Get_Account_Info"
        url = f'/accountinfo/app_ID/{app_id_param}/secret/{app_secret_param}/account/{account}'
        info = logger_in(fun, ic_code, code_app, url)

        mktrep = MarketRep(app_id=app_id_param, app_secret=app_secret_param,
                           broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = mktrep.Derivatives()

        account_info = deri.get_account_info(account_no=account)

        if account_info:
            fun = "Ret_Account_Info"
            info = logger_out(fun, ic_code, code_app, account_info)
            return account_info
    except SettradeError as e:
        # logger.error(f"SettradeError occurred: {str(e)}")
        fun = "Error_Account_Info"
        errorvalue = f'Error : {str(e.status_code)} ,detail: {str(e.args)}'
        info = logger_error(fun, ic_code, code_app, errorvalue)
        raise HTTPException(status_code=e.status_code, detail=e.args)
# Get Account Info ดึงข้อมูล account information End

# Get Portfolios ดึงข้อมูล portfolio (สัญญาที่เปิดอยู่) จาก derivatives object Start


@router.get("/app_ID/{app_id_param}/secret/{app_secret_param}/portfolios/{account}")
def Get_Portfolios(account: str, ic_code: str, code_app: str, app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)

    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(
            status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        fun = 'Get_Portfolios'
        url = f'/app_ID/{app_id_param}/secret/{app_secret_param}/portfolios/{account}'
        info = logger_in(fun, ic_code, code_app, url)

        mktrep = MarketRep(app_id=app_id_param, app_secret=app_secret_param,
                           broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = mktrep.Derivatives()
        portfolios = deri.get_portfolios(account_no=account)

        if (portfolios):
            fun = 'Ret_Portfolios'
            info = logger_out(fun, ic_code, code_app, portfolios)
            return portfolios
    except SettradeError as e:
        fun = 'Error_Portfolios'
        errorvalue = f'Error : {str(e.status_code)} ,detail: {str(e.args)}'
        info = logger_error(fun, ic_code, code_app, errorvalue)
        raise HTTPException(status_code=e.status_code, detail=e.args)
# Get Portfolios ดึงข้อมูล portfolio (สัญญาที่เปิดอยู่) จาก derivatives object End


# Get Order ดึงข้อมูล order ตาม orderNo Start
@router.get("/app_ID/{app_id_param}/secret/{app_secret_param}/orderNo/{order_no}")
def Get_Order(order_no: int, ic_code: str, code_app: str, app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)

    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(
            status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        fun = 'Get_Order'
        url = f'/app_ID/{app_id_param}/secret/{app_secret_param}/orderNo/{order_no}'
        info = logger_in(fun, ic_code, code_app, url)

        mktrep = MarketRep(app_id=app_id_param, app_secret=app_secret_param,
                           broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = mktrep.Derivatives()
        order = deri.get_order(order_no=order_no)
        if (order):
            fun = 'Ret_Order'
            info = logger_out(fun, ic_code, code_app, order)
            return order
    except SettradeError as e:
        fun = 'Error_Order'
        errorvalue = f'Error : {str(e.status_code)} ,detail: {str(e.args)}'
        info = logger_error(fun, ic_code, code_app, errorvalue)
        raise HTTPException(status_code=e.status_code, detail=e.args)
# Get Order ดึงข้อมูล order ตาม orderNo End

# Get Orders ดึงข้อมูล order ทั้งหมด Start


@router.get("/app_ID/{app_id_param}/secret/{app_secret_param}")
def Get_Orders(ic_code: str, code_app: str, app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)

    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(
            status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        fun = 'Get_Orders'
        url = f'/app_ID/{app_id_param}/secret/{app_secret_param}'
        info = logger_in(fun, ic_code, code_app, url)

        mktrep = MarketRep(app_id=app_id_param, app_secret=app_secret_param,
                           broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = mktrep.Derivatives()
        orders = deri.get_orders()
        if (orders):
            fun = 'Ret_Orders'
            info = logger_out(fun, ic_code, code_app, orders)
            return orders
    except SettradeError as e:
        fun = 'Error_Orders'
        errorvalue = f'Error : {str(e.status_code)} ,detail: {str(e.args)}'
        info = logger_error(fun, ic_code, code_app, errorvalue)
        raise HTTPException(status_code=e.status_code, detail=e.args)
# Get Orders ดึงข้อมูล order ทั้งหมด End

# Get Orders By Account Number ดึงข้อมูล order ทั้งหมดจาก derivatives object เฉพาะของ account number Start


@router.get("/app_ID/{app_id_param}/secret/{app_secret_param}/account_No/{account}")
def Get_Orders_By_Account_Number(account: str, ic_code: str, code_app: str, app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)

    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(
            status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        fun = 'Get_Orders_By_Account'
        url = f'/app_ID/{app_id_param}/secret/{app_secret_param}/account_No/{account}'
        info = logger_in(fun, ic_code, code_app, url)

        mktrep = MarketRep(app_id=app_id_param, app_secret=app_secret_param,
                           broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = mktrep.Derivatives()
        order_list = deri.get_orders_by_account_no(account_no=account)
        if (order_list):
            fun = 'Ret_Orders_By_Account'
            info = logger_out(fun, ic_code, code_app, order_list)
            return order_list
    except SettradeError as e:
        fun = 'Error_Orders_By_Account'
        errorvalue = f'Error : {str(e.status_code)} ,detail: {str(e.args)}'
        info = logger_error(fun, ic_code, code_app, errorvalue)
        raise HTTPException(status_code=e.status_code, detail=e.args)
# Get Orders By Account Number ดึงข้อมูล order ทั้งหมดจาก derivatives object เฉพาะของ account number End

# Get Trades ดึงข้อมูล trade ทั้งหมด จาก derivatives object Start


@router.get("/app_ID/{app_id_param}/secret/{app_secret_param}/trades/{account}")
def Get_Trades(account: str, ic_code: str, code_app: str, app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)

    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(
            status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        fun = 'Get_Trades'
        url = f'/app_ID/{app_id_param}/secret/{app_secret_param}/trades/{account}'
        info = logger_in(fun, ic_code, code_app, url)

        mktrep = MarketRep(app_id=app_id, app_secret=app_secret,
                           broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = mktrep.Derivatives()
        trade_list = deri.get_trades(account_no=account)
        if (trade_list):
            fun = 'Ret_Trades'
            info = logger_out(fun, ic_code, code_app, trade_list)
            return trade_list
    except SettradeError as e:
        fun = 'Error_Trades'
        errorvalue = f'Error : {str(e.status_code)} ,detail: {str(e.args)}'
        info = logger_error(fun, ic_code, code_app, errorvalue)
        raise HTTPException(status_code=e.status_code, detail=e.args)
# Get Trades ดึงข้อมูล trade ทั้งหมด จาก derivatives object End

# Place Order ส่ง/วาง order จากนั้นจะได้ order object กลับมา Start


@router.post("/order")
# def Place_Order(account:str,account_no:str, symbol:str, side:str, position:str, price_type:str, price:float, volume:int, validity_type:str, iceberg_vol:int, validity_date_condition:str|None == None, stop_condition:str, stop_symbol:str, stop_price:float, trigger_session:str, bypass_warning:bool):
# def Place_Order(app_id_param: Optional[str], app_secret_param: Optional[str],ic_code:str,code_app:str,data: Dict[str, Any] = Body(...)):
def Place_Order(app_id_param: Optional[str], app_secret_param: Optional[str], ic_code: str, code_app: str, data: OrderRequest):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)

    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(
            status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        fun = 'Set_Place_Order'
        url = f'/order'
        info = logger_in(fun, ic_code, code_app, url)

        mktrep = MarketRep(app_id=app_id, app_secret=app_secret,
                           broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = mktrep.Derivatives()
        # order = deri.place_order(
        #     account_no="119871-4",
        #     symbol="KTCZ23",
        #     side="Long",
        #     position="Open",
        #     price_type="Limit",
        #     price=45.50,
        #     volume=20,
        #     stopCondition="ASK_OR_HIGHER",
        #     triggerSession="Pre-Open1",
        #     bypassWarning=True
        # )
        order = deri.place_order(
            account_no = data.account_no,
            symbol = data.symbol,
            side = data.side,
            position = data.position,
            price_type = data.price_type,
            price = data.price,
            volume = data.volume,
            validity_type = data.validity_type,
            iceberg_vol = data.iceberg_vol,
            validity_date_condition = data.validity_date_condition,
            stop_condition = data.stop_condition,
            stop_symbol = data.stop_symbol,
            stop_price = data.stop_price,
            trigger_session = data.trigger_session,
            bypass_warning = data.bypass_warning)

        if (order):
            fun = 'Ret_Place_Order'
            Header = f'Header : {app_id_param},{app_secret_param} : Body :'
            info = logger_body(fun, ic_code, code_app, Header, order)
            return order
    except SettradeError as e:
        fun = 'Error_Place_Order'
        errorvalue = f'Error : {str(e.status_code)} ,detail: {str(e.args)}'
        info = logger_error(fun, ic_code, code_app, errorvalue)
        raise HTTPException(status_code=e.status_code, detail=e.args)
# Place Order ส่ง/วาง order จากนั้นจะได้ order object กลับมา End

# Change Order  เปลี่ยนข้อมูล order ที่ส่งไปจาก place order Start


@router.put('/changorder')
def Chang_Order(body: ChangOrder, ic_code: str, code_app: str, app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)

    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(
            status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        fun = 'Set_Change_Order'
        url = f'/changorder'
        info = logger_in(fun, ic_code, code_app, url)

        mktrep = MarketRep(app_id=app_id, app_secret=app_secret,
                           broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = mktrep.Derivatives()
        chang_order = deri.change_order(
            account_no=body.account_no,
            order_no=body.order_no,
            new_price=body.new_price,
            new_volume=body.new_volume,
            bypass_warning=body.bypass_warning,
        )
        fun = 'Ret_Change_Order'
        Header = f'Header : {app_id_param},{app_secret_param}'
        Bodys = f'Bodys : { account_no:{body.account_no},order_no:{body.order_no},new_price:{body.new_price},new_volume:{body.new_volume},bypass_warning:{body.bypass_warning} }'
        info = logger_body(fun, ic_code, code_app, Header, Bodys)
        return chang_order
    except SettradeError as e:
        fun = 'Error_Change_Order'
        errorvalue = f'Error : {str(e.status_code)} ,detail: {str(e.args)}'
        info = logger_error(fun, ic_code, code_app, errorvalue)
        raise HTTPException(status_code=e.status_code, detail=e.args)
# Change Order  เปลี่ยนข้อมูล order ที่ส่งไปจาก place order End

# Cancel Order ยกเลิก order Start


@router.put('/cancelorder')
async def Cancel_Order(account: str, order: int, ic_code: str, code_app: str, app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)

    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(
            status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        fun = 'Set_Cancel_Order'
        url = f'/cancelorder'
        info = logger_in(fun, ic_code, code_app, url)
        mktrep = MarketRep(app_id=app_id_param, app_secret=app_secret_param,
                           broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = mktrep.Derivatives()
        cancel_order = deri.cancel_order(account_no=account, order_no=order)

        fun = 'Ret_Cancel_Order'
        Header = f'{account},{order},{app_id_param},{app_secret_param}'
        info = logger_out(fun, ic_code, code_app, Header)
        return {"msg": f"Cancel Order No {order} Success. And Doc Return Empty dictionary."}
    except SettradeError as e:
        fun = 'Error_Cancel_Order'
        errorvalue = f'Error : {str(e.status_code)} ,detail: {str(e.args)}'
        info = logger_error(fun, ic_code, code_app, errorvalue)
        raise HTTPException(status_code=e.status_code, detail=e.args)
# Cancel Order ยกเลิก order End

# Cancel Orders ยกเลิก order มากกว่า 1 order Start


@router.put('/cancelorders')
async def Cancel_Orders(account: str, orders_no: ItemOrderNo, ic_code: str, code_app: str, app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)

    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(
            status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        fun = 'Set_Cancel_Orders'
        url = f'/cancelorders'
        info = logger_in(fun, ic_code, code_app, url)

        mktrep = MarketRep(app_id=app_id_param, app_secret=app_secret_param,
                           broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = mktrep.Derivatives()
        cancel_orders = deri.cancel_orders(
            account_no=account, order_no_list=orders_no.orders_no)
        if (cancel_orders):
            fun = 'Ret_Cancel_Orders'
            info = logger_out(fun, ic_code, code_app, cancel_orders)
            return cancel_orders
    except SettradeError as e:
        fun = 'Error_Cancel_Orders'
        errorvalue = f'Error : {str(e.status_code)} ,detail: {str(e.args)}'
        info = logger_error(fun, ic_code, code_app, errorvalue)
        raise HTTPException(status_code=e.status_code, detail=e.args)
# Cancel Orders ยกเลิก order มากกว่า 1 order End

# Place Trade Report ส่ง place trade report Start


@router.post("/tradereport")
def Place_Trade_Report(account: str, ic_code: str, code_app: str, ord_no: str, data_report: PlaceTradeReport, app_id_param: str, app_secret_param: str):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if (data_report.seller == "None" or data_report.seller == "string" or data_report.seller == ""):
        data_report.seller = None
    if (data_report.control_key == "0"):
        data_report.control_key = 0
    if (data_report.buyer == "None" or data_report.buyer == "string" or data_report.buyer == "" ):
        data_report.buyer = None

    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)
    
    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(
            status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        fun = 'Get_Place_Trade_Report'
        url = f'/tradereport'
        info = logger_in_Trade_report(fun, ic_code, code_app, ord_no, url)
    
        mktrep = MarketRep(app_id=app_id_param, app_secret=app_secret_param,
                           broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = mktrep.Derivatives()
        place_trade_report = deri.place_trade_report(
            symbol=data_report.symbol,
            position=data_report.position,
            price=data_report.price,
            volume=data_report.volume,
            cpm=data_report.cpm,
            ty_type=data_report.ty_type,
            buyer=data_report.buyer,
            seller=data_report.seller,
            control_key=data_report.control_key
        )
        if (place_trade_report):
            fun = 'Set_Place_Trade_Report'
            Header = f'Header : {account},{app_id_param},{app_secret_param}'
            Bodys = f'Bodys : symbol:{data_report.symbol},position:{data_report.position},price:{data_report.price},volume:{data_report.volume},cpm:{data_report.cpm},ty_type:{data_report.ty_type},buyer:{data_report.buyer},seller:{data_report.seller},control_key:{data_report.control_key},Return:{place_trade_report}'
            info = logger_Trade(fun, ic_code, code_app, ord_no, Header, Bodys)
            return place_trade_report
    except SettradeError as e:
        fun = 'Error_Place_Trade_Report'
        errorHeader = f'Header : {account},{app_id_param},{app_secret_param}'
        errorBody = f'Bodys : symbol:{data_report.symbol},position:{data_report.position},price:{data_report.price},volume:{data_report.volume},cpm:{data_report.cpm},ty_type:{data_report.ty_type},buyer:{data_report.buyer},seller:{data_report.seller},control_key:{data_report.control_key}'
        errorvalue = f'Error : {str(e.status_code)} ,detail: {str(e.args)}'
        info = logger_Trade_error(fun, ic_code, code_app, ord_no,errorHeader,errorBody, errorvalue)
        raise HTTPException(status_code=e.status_code, detail=e.args)
# Place Trade Report ส่ง place trade report End


@router.get('/maket_data')
def Initialize_Maket_Data(ic_code: str, code_app: str, app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)

    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(
            status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        fun = 'Get_Maket_Data'
        url = f'/maket_data'
        info = logger_in(fun, ic_code, code_app, url)

        mktrep = MarketRep(app_id=app_id_param, app_secret=app_secret_param,
                           broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = mktrep.MarketData()

        if (deri):
            fun = 'Ret_Maket_Data'
            info = logger_out(fun, ic_code, code_app, deri._ctx)
            return deri
    except SettradeError as e:
        fun = 'Error_Maket_Data'
        errorvalue = f'Error : {str(e.status_code)} ,detail: {str(e.args)}'
        info = logger_error(fun, ic_code, code_app, errorvalue)
        raise HTTPException(status_code=e.status_code, detail=e.args)


@router.get('/quote_symbol')
def Get_Quote_Symbol(symbol: str, app_id_param: Optional[str] = None, app_secret_param: Optional[str] = None):
    # If app_id_param and app_secret_param are provided in the request, update the global values
    if app_id_param and app_secret_param:
        change_credentials(app_id_param, app_secret_param)

    # Check if app_id and app_secret are available
    if not app_id or not app_secret:
        raise HTTPException(
            status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
    try:
        mktrep = MarketRep(app_id=app_id_param, app_secret=app_secret_param,
                           broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
        deri = mktrep.MarketData()
        # market = marketrep.MarketData()
        market = deri.get_quote_symbol(symbol)
        if (market):
            return market
    except SettradeError as e:
        raise HTTPException(status_code=e.status_code, detail=e.args)

# Place Order ส่ง/วาง order จากนั้นจะได้ order object กลับมา Start

# def Place_Order(app_id_param: Optional[str], app_secret_param: Optional[str],ic_code:str,code_app:str,data:OrderRequest):


# @router.post("/Test_order")
# def Test_Place_Order():
#     # If app_id_param and app_secret_param are provided in the request, update the global values
#     app_id_param = "AjeT5okzYPZUG91r"
#     app_secret_param = "MyGrJMt7Crmnly1WU8ce8E4n3CMUJ+Psxl04q1xl8eo="
#     ic_code = "IC_Test"
#     code_app = "Mobile"
#     if app_id_param and app_secret_param:
#         change_credentials(app_id_param, app_secret_param)

#     # Check if app_id and app_secret are available
#     if not app_id or not app_secret:
#         raise HTTPException(
#             status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
#     try:
#         fun = 'Test_Set_Place_Order'
#         url = f'/Test_order'
#         info = logger_in(fun, ic_code, code_app, url)

#         mktrep = MarketRep(app_id=app_id, app_secret=app_secret,
#                            broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)

#         deri = mktrep.Derivatives()
#         order = deri.place_order(
#             account_no="207329-4",
#             symbol="S50Z23",
#             side="Long",
#             position="Open",
#             price_type="Limit",
#             price=880.7,
#             volume=1,
#             validity_type="Day",
#         )
#         print(f"{order}")
#         # order = deri.place_order(
#         #     account_no = data.account_no,
#         #     symbol = data.symbol,
#         #     side = data.side,
#         #     position = data.position,
#         #     price_type = data.price_type,
#         #     price = data.price,
#         #     volume = data.volume,
#         #     validity_type = data.validity_type,
#         #     iceberg_vol = data.iceberg_vol,
#         #     validity_date_condition = data.validity_date_condition,
#         #     stop_condition = data.stop_condition,
#         #     stop_symbol = data.stop_symbol,
#         #     stop_price = data.stop_price,
#         #     trigger_session = data.trigger_session,
#         #     bypass_warning = data.bypass_warning)

#         if (order):
#             fun = 'Ret_Place_Order'
#             Header = f'Header : {app_id_param},{app_secret_param} : Body :'
#             info = logger_body(fun, ic_code, code_app, Header, order)
#             return order
#     except SettradeError as e:
#         fun = 'Error_Place_Order'
#         errorvalue = f'Error : {str(e.status_code)} ,detail: {str(e.args)}'
#         info = logger_error(fun, ic_code, code_app, errorvalue)
#         print(e.status_code, e.args)
#         raise HTTPException(status_code=e.status_code, detail=e.args)
# # Place Order ส่ง/วาง order จากนั้นจะได้ order object กลับมา End


# @router.post("/test_trade_report")
# def Test_Place_Trade_Report():
#     app_id_param = "AjeT5okzYPZUG91r"
#     app_secret_param = "MyGrJMt7Crmnly1WU8ce8E4n3CMUJ+Psxl04q1xl8eo="
#     ic_code = "IC_Test"
#     code_app = "Mobile"
#     ord_no = "oo01"
#     # If app_id_param and app_secret_param are provided in the request, update the global values
#     if app_id_param and app_secret_param:
#         change_credentials(app_id_param, app_secret_param)

#     # Check if app_id and app_secret are available
#     if not app_id or not app_secret:
#         raise HTTPException(
#             status_code=400, detail="App credentials are not set. Please provide app_id and app_secret.")
#     try:
#         fun = 'Get_Place_Trade_Report'
#         url = '/Test_trade_report'
#         info = logger_in_Trade_report(fun, ic_code, code_app, ord_no, url)
#         mktrep = MarketRep(app_id=app_id_param, app_secret=app_secret_param,
#                            broker_id=broker_id, app_code=app_code, is_auto_queue=is_auto_queue)
#         deri = mktrep.Derivatives()
#         place_trade_report = deri.place_trade_report(
#             symbol="S50Z23",
#             position="Open",
#             price=881.2,
#             volume=100,
#             cpm="0029",
#             ty_type="TX SET50 Futures",
#             buyer="207329-4",
#             seller=None,
#             control_key=0
#         )
#         if (place_trade_report):
#             fun = 'Set_Place_Trade_Report'
#             # Header = f'Header : {account},{app_id_param},{app_secret_param}'
#             # Bodys = f'Bodys : symbol:{report.symbol},position:{report.position},price:{report.price},volume:{report.volume},cpm:{report.cpm},tr_type:{report.tr_type},buyer:{report.buyer},seller:{report.seller},control_key:{report.control_key},Return:{place_trade_report}'
#             # info = logger_Trade(fun, ic_code, code_app, ord_no, Header, Bodys)
#             return place_trade_report
#     except SettradeError as e:
#         fun = 'Error_Place_Trade_Report'
#         errorvalue = f'Error : {str(e.status_code)} ,detail: {str(e.args)}'
#         info = logger_Trade_error(fun, ic_code, code_app, ord_no, errorvalue)
#         print(e.status_code, e.args)
#         raise HTTPException(status_code=e.status_code, detail=e.args)
# Place Trade Report ส่ง place trade report End
