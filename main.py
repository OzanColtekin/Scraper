
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import os
from Database import Database
from products import Product


class Trendyol:
    def __init__(self, findkeyword, catid):
        self.keyword = findkeyword
        self.url = "https://www.trendyol.com/sr?q=" + str(self.keyword) + "&st=" + str(self.keyword) + "&qt=" + str(
            self.keyword) + "&os=1&pi="
        self.productLinks = []
        self.catID = catid
        self.dataFrame = pd.DataFrame(columns=['barcode', 'productBrand', 'productName', 'ratingCount', 'favories',
                                               'sellerPoint', 'price', 'productPoint', 'isFreeCargo',
                                               'sellerStock', 'date'])
        self.databse = Database('OZAN\OZANMSSQL19', 'hizlianaliz_core', 'sa', 'ozan_1907')

    def gotourl(self, url, x=0):
        self.html = requests.get(url + str(x)).content
        self.soup = BeautifulSoup(self.html, "html.parser")
        if url != self.url:
            self.script = self.soup.findAll("script")
            self.sellerName = self.soup.find("a", {"class": "merchant-text"}).text
            self.product = str(self.script).split('"name":"' + self.sellerName + '"')

    def appendproductlinks(self):
        links = self.soup.find_all("div", {"class": "p-card-chldrn-cntnr"})
        for link in links:
            self.productLinks.append("https://www.trendyol.com" + str(link).split("<a href=")[1].split('"')[1])

    def getproductlinks(self):
        self.productLinks = []
        for x in range(0, 6):
            self.gotourl(self.url, x)
            self.appendproductlinks()
        self.getproductdetail()

    def getproductdetail(self):
        for url in self.productLinks:
            self.gotourl(url)
            """
            addProduct = {"barcode": self.findproductbarcode(),
                          "productBrand": self.findproductbrand(),
                          "productName": self.findproductname(),
                          "ratingCount": self.findratingcount(),
                          "favories": self.findfavoriescount(),
                          "sellerPoint": self.findsellerpoint(),
                          "price": self.findproductprice(),
                          "productPoint": self.findproductpoint(),
                          "isFreeCargo": self.isfreecargo(),
                          "sellerStock": self.sellerstock(),
                          "date": str(str(datetime.datetime.now()).split(".")[0])
            }
            """
            addProduct = Product(self.findproductbarcode(), self.findproductbrand(), self.findproductname(),
                                 self.findproductpoint(), self.findfavoriescount(), self.findsellerpoint(),
                                 self.isfreecargo(), self.findratingcount(), self.findproductprice(),
                                 str(str(datetime.datetime.now()).split(".")[0]), 1, self.catID,self.findCargoRemainingDay(),
                                 self.findFeauturesCount(),self.findphotonumber(),self.findSellersCount())
            self.databse.addproduct(addProduct)
            #self.dataFrame = self.dataFrame.append(addProduct, ignore_index=True)
        #self.savetocsv()

    def findDescWordCount(self):
        descr=self.soup.find("div",{"class":"info-wrapper"})
        detailDesc=str(descr).split('<ul class="detail-desc-list"><li>')[1].split(' ')
        descWordCount=len(detailDesc)
        return descWordCount

    def findSellersCount(self):
        try:
            otherSellers = self.soup.find("div", {"class": "pr-omc-tl title"})
            sellersCount = int(otherSellers.text.split("(")[1].split(")")[0]) + 1
        except:
            sellersCount = 1
        return sellersCount

    def findphotonumber(self):
        try:
            photoLinks=self.soup.find_all("div",{"class":"styles-module_slider__o0fqa"})
            photoNumber = len(str(photoLinks).split("<img alt="))-1
            if(photoNumber==0):
                photoNumber=1
        except:
            photoNumber = 0
        return int(photoNumber)
    
    def findFeauturesCount(self):
        try:
            detailContainer=self.soup.find("div",{"class":"detail-border"})
            detailFeatures=(str(detailContainer).split('<ul class="detail-attr-container">')[1])
            feautures=detailFeatures.split('<li class="detail-attr-item"')
            feauturesCount=len(feautures)-1
        except:
            feauturesCount=0
        return feauturesCount

    def findCargoRemainingDay(self):
        cargoRemainingDays=(str(self.product).split('"cargoRemainingDays"')[1].split(',')[0].strip(':'))
        return cargoRemainingDays

    def findproductbarcode(self):
        try:
            barcode = self.product[len(self.product) - 2].split('"barcode":')[1].split(",")[0]
        except:
            barcode = 0
        return str(barcode.strip('"').split('"')[0])

    def findproductname(self):
        title = self.soup.find("h1", {"class": "pr-new-br"})
        try:
            if '<a href="' in str(title) != -1:
                productName = str(title).split('<span>')[1].split('</span>')[0]
            else:
                productName = str(title).split('<span>')[1].split('</span>')[0]
        except:
            productName = title.text

        return str(productName.replace("'", " "))

    def findproductbrand(self):
        title = self.soup.find("h1", {"class": "pr-new-br"})
        try:
            if '<a href="' in str(title) != -1:
                productBrand = str(title).split('"h1">')[1].split('>')[1].split('<')[0]
            else:
                productBrand = str(title).split('"h1">')[1].split('<')[0]
        except:
            productBrand = "Kayıtsız Marka"

        return str(productBrand)

    def findratingcount(self):
        try:
            ratingCount = self.soup.find("div", {"class": "pr-in-rnr"}).text
            ratingCount = ratingCount.split("Değerlendirme")[0]
        except:
            ratingCount = 0
        return int(ratingCount)

    def findfavoriescount(self):
        try:
            favories = self.soup.find("div", {"class": "fv-dt"}).text
            favories = favories.split("favori")[0]
        except:
            favories = 0
        return int(favories)

    def findsellerpoint(self):
        try:
            sellerpoint = self.product[len(self.product) - 1].split('"sellerScore":')[1].split(",")[0]
        except:
            sellerpoint = 0
        return float(sellerpoint)

    def findproductpoint(self):
        try:
            productpoint = self.product[len(self.product) - 1].split('"averageRating":')[1].split(",")[0]
        except:
            productpoint = 0
        return float(productpoint)

    def sellerscount(self):
        try:
            otherSellers = self.soup.find("div", {"class": "pr-omc-tl title"})
            sellersCount = int(otherSellers.text.split("(")[1].split(")")[0]) + 1
        except:
            sellersCount = 1
        return sellersCount

    def isfreecargo(self):
        try:
            isFreeCargo = self.product[len(self.product) - 2].split('"isFreeCargo":')[1].split(",")[0]
            if isFreeCargo == "true":
                isFreeCargo = 1
            else:
                isFreeCargo = 0
        except:
            isFreeCargo = 0
        return isFreeCargo

    def sellerstock(self):
        try:
            sellerStock = self.product[len(self.product) - 2].split("satılmak üzere")[1].split("adetten")[0]
        except:
            sellerStock = 0
        return int(sellerStock)

    def findproductprice(self):
        productPrice = self.soup.find("div", {"class": "product-price-container"}).text
        if productPrice.find("Sepet Fiyatı") != - 1 :
            productPrice = productPrice.split("Sepet Fiyatı")[1]
        if productPrice.find("İndirim") != -1:
            productPrice = productPrice.split("İndirim")[1]
        elif productPrice.find("%") != -1:
            productPrice = productPrice.split("%")[1].split(" TL")[0]
        else:
            productPrice = productPrice
        productPrice = productPrice.split(' TL')[0].split(',')[0]
        if productPrice.find(".") != -1:
            carpim = 10 ** (len(productPrice.split(".")[1]))
            productPrice = float(productPrice.split(",")[0])
            productPrice = carpim * productPrice
        return int(productPrice)

    def savetocsv(self):
        self.path = r"C:\\Users\\ayhan\\OneDrive\\Masaüstü\\main\\categories\\"+self.keyword+r"\\"
        if (os.path.isdir(self.path) != True):
            os.mkdir(self.path)
        self.dataFrame.to_csv(self.path + self.keyword +" "+ str(str(datetime.datetime.now()).split(".")[0].split(" ")[0]) + " dataset.csv")

    def start_schedules(self):
        schedule.every().days.at("23:43").do(self.getproductlinks)