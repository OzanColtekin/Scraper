from RankFinder import RankFinder
from Database import Database
import datetime
import threading
from PriceFinder import Price

db = Database('OZAN\OZANMSSQL19', 'hizlianaliz', 'sa', 'pass')

def updateRank():
  threading.Timer(120.0, updateRank).start()
  for prd in db.getRankUrl():
    rank = RankFinder(prd[0],prd[1]).getRank() if RankFinder(prd[0],prd[1]).getRank() != None else 0
    db.updateRank(prd[0],prd[1],rank,str(str(datetime.datetime.now()).split(".")[0]))


def GetPrice():
  threading.Timer(15.0, GetPrice).start()
  for prd in db.getPriceUrl():
    productPrice = Price(prd[0]).getPrice()
    db.savePrice(productBarcode="0",productUrl=prd[0],price=productPrice,Date=str(str(datetime.datetime.now()).split(".")[0]))



#updateRank()
GetPrice()