class Product:
    def __init__(self, pbarcode, pbrand, pname, ppoint, pfav, pselpoint, pcargo, prating, pprice, pdate, pstatus, pcategory, pCargoRemainingDay, pFeaturesCount, pPhotoCount, pSallerCount):
        self.ProductBarcode = pbarcode
        self.ProductBrand = pbrand
        self.ProductName = pname
        self.ProductPoint = ppoint
        self.Favories = pfav
        self.SellerPoint = pselpoint
        self.IsFreeCargo = pcargo
        self.RatingCount = prating
        self.Price = pprice
        self.Date = pdate
        self.Status = pstatus
        self.CategoryID = pcategory
        self.CargoRemainingDay = pCargoRemainingDay
        self.FeaturesCount = pFeaturesCount
        self.PhotoCount = pPhotoCount
        self.SallerCount = pSallerCount