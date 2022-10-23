import pyodbc

class Database:
    def __init__(self, hostname, database, username, password):
        self.hostname = hostname
        self.database = database
        self.username = username
        self.password = password
        self.connection = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=' + self.hostname + ';DATABASE=' + self.database + ';UID=' +
            self.username + ';PWD=' + self.password)
        self.cursor = self.connection.cursor()
    
    def savechanges(self):
        self.cursor.execute(self.sql)
        self.connection.commit()

    def addproduct(self, product):
        self.sql = f"INSERT INTO Products(ProductBarcode, ProductBrand, ProductName, ProductPoint, Favories," \
                   f" SellerPoint, IsFreeCargo, RatingCount, CategoryID, Price, Date, Status, CargoRemainingDay, FeaturesCount, PhotoCount, SallerCount) VALUES " \
                   f"('{product.ProductBarcode}', '{product.ProductBrand}', '{product.ProductName}', " \
                   f"'{product.ProductPoint}', '{product.Favories}', '{product.SellerPoint}', " \
                   f"'{product.IsFreeCargo}', '{product.RatingCount}', '{product.CategoryID}', " \
                   f"'{product.Price}', '{product.Date}', '{product.Status}', '{product.CargoRemaininDay}', '{product.FeaturesCount}', '{product.PhotoCount}', '{product.SallerCount}')"
        self.savechanges()
    
    def getRankUrl(self):
        self.sql = "Select ProductLink, Keyword from ProductRanks"
        rows = self.cursor.execute(self.sql).fetchall()
        return rows
    
    def updateRank(self,productUrl,Keyword,rank,dt):
        self.sql = f"Update ProductRanks set RankNumber='{rank}', Date='{dt}' where ProductLink='{productUrl}' and Keyword='{Keyword}'"
        self.savechanges()

    def getPriceUrl(self):
        self.sql = f"Select ProductUrl from UserProductsPrices"
        rows = self.cursor.execute(self.sql).fetchall()
        return rows
    
    def savePrice(self,productBarcode,productUrl,price,Date):
        self.sql = f"INSERT INTO ProductPrices(ProductBarcode, ProductUrl, Price, Date)" \
                   f"VALUES ('{productBarcode}', '{productUrl}', '{price}', '{Date}')"
        self.savechanges()
    
    def addCategorie(self,categoryName,trendyolID):
        self.sql = f"INSERT INTO Categories(CategoryName,TrendyolID) VALUES ('{categoryName}', '{trendyolID}')"
        self.savechanges()