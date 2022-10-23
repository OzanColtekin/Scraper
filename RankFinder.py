import requests
from bs4 import BeautifulSoup

class RankFinder():
    def __init__(self,url,keyword):
        self.product = url.split("?boutiqueId")[0]
        self.kwargs = keyword
        self.url = f"https://www.trendyol.com/sr?q={keyword}&st={keyword}&qt={keyword}&os=1&pi="
        self.productLinks = []
        self.rank = 1
    
    def getRank(self):
        for x in range(100):
            self.html=requests.get(self.url+str(x)).content
            self.soup=BeautifulSoup(self.html,"html.parser")
            links = self.soup.find_all("div",{"class":"p-card-chldrn-cntnr"})
            for link in links:
                prdct = "https://www.trendyol.com"+str(link).split("<a href=")[1].split('"')[1].split("?boutiqueId")[0]
                if self.product == prdct:
                    return self.rank
                else :
                    self.rank += 1