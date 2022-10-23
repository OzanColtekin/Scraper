import requests
from bs4 import BeautifulSoup

class Price():
    def __init__(self,url):
        self.html = requests.get(url).content
        self.soup = BeautifulSoup(self.html, "html.parser")
    
    def getPrice(self):
        productPrice = self.soup.find("div", {"class": "product-price-container"}).text
        if productPrice.find("Sepet Fiyatı") != - 1 :
            productPrice = productPrice.split("Sepet Fiyatı")[1]
        if productPrice.find("İndirim") != -1:
            productPrice = productPrice.split("İndirim")[1]
        else:
            productPrice = productPrice
        productPrice = productPrice.split(' TL')[0].split(',')[0]
        if productPrice.find(".") != -1:
            carpim = 10 ** (len(productPrice.split(".")[1]))
            productPrice = float(productPrice.split(",")[0])
            productPrice = carpim * productPrice
        return int(productPrice)

