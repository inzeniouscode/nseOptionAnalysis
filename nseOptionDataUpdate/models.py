from django.db import models

# Create your models here.
# Create your models here.
class nseOptionData(models.Model):
    underlying  = models.CharField(max_length=64)
    strikePrice = models.IntegerField()
    expiryDate  = models.DateField() 
    underlyingValue = models.FloatField(null=True)
    identifierCall  = models.CharField(max_length=128,null=True)    
    openInterestCall = models.IntegerField(null=True)
    changeinOpenInterestCall = models.IntegerField(null=True)
    pchangeinOpenInterestCall = models.FloatField(null=True)
    totalTradedVolumeCall = models.IntegerField(null=True)
    impliedVolatilityCall = models.FloatField(null=True)
    lastPriceCall = models.FloatField(null=True)
    changeCall = models.FloatField(null=True)
    pChangeCall = models.FloatField(null=True)
    totalBuyQuantityCall = models.IntegerField(null=True)
    totalSellQuantityCall = models.IntegerField(null=True)
    bidQtyCall = models.IntegerField(null=True)
    bidpriceCall = models.FloatField(null=True)
    askQtyCall = models.IntegerField(null=True)
    askPriceCall = models.FloatField(null=True)
    identifierPut  = models.CharField(max_length=128,null=True)    
    openInterestPut = models.IntegerField(null=True)
    changeinOpenInterestPut = models.IntegerField(null=True)
    pchangeinOpenInterestPut = models.FloatField(null=True)
    totalTradedVolumePut = models.IntegerField(null=True)
    impliedVolatilityPut = models.FloatField(null=True)
    lastPricePut = models.FloatField(null=True)
    changePut = models.FloatField(null=True)
    pChangePut = models.FloatField(null=True)
    totalBuyQuantityPut = models.IntegerField(null=True)
    totalSellQuantityPut = models.IntegerField(null=True)
    bidQtyPut = models.IntegerField(null=True)
    bidpricePut = models.FloatField(null=True)
    askQtyPut = models.IntegerField(null=True)
    askPricePut = models.FloatField(null=True)
    recordCreated = models.DateTimeField(auto_now_add=True,blank=True)
    recordUpdated = models.DateTimeField(auto_now_add=True,blank=True)

    class Meta:
        db_table = 'nseOptionData'

    def __str__(self):
        return str(self.id)

