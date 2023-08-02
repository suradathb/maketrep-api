# models/data_item.py
from pydantic import BaseModel

class AccountInfo(BaseModel):
    callForceFlag: str
    callForceMargin: float
    callForceMarginMM: float
    cashBalance: float
    closingMethod: str
    creditLine: float
    depositWithdrawal: float
    equity: float
    excessEquity: float
    initialMargin: float
    liquidationValue: float
    totalFM: float
    totalMM: float
    totalMR: float
