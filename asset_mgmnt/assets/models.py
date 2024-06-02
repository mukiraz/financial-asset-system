from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    is_liquid = models.BooleanField(default=True)
    description = models.TextField(null=True, blank = True)
    is_delatable = models.BooleanField(default = True)
    is_auto_updated = models.BooleanField(default = True, null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name
    
class Currency(models.Model):
    currency_code = models.CharField(max_length=10)
    currency_name = models.CharField(max_length=100)
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.currency_code
    
class UnitType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name
    
class SwissStockHTMLContent(models.Model):
    html_content = models.TextField()

    def __str__(self):
        return str(self.pk)
    
class AssetType(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    current_price = models.FloatField() 
    description = models.TextField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.name}"
    
class Account(models.Model):
    name = models.CharField(max_length=100)
    iban = models.CharField(max_length=50, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name
    
class ExchangeRate(models.Model):
    from_currency_id = models.ForeignKey(Currency, related_name='from_currency_id', on_delete=models.CASCADE)
    to_currency_id = models.ForeignKey(Currency, related_name='to_currency_id', on_delete=models.CASCADE)
    rate = models.FloatField()
    rate_date = models.DateField()
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return  f"{self.from_currency_id} - {self.to_currency_id}"
    
class Asset(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    buy_date = models.DateField(null=True, blank=True)
    buy_unit_price = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    number =  models.FloatField()
    unit_type = models.ForeignKey(UnitType, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)

    @property
    def current_price(self):
        current_price = self.asset_type.current_price
        return  current_price
    
    @property
    def cost(self):
        cost = self.number * self.buy_unit_price
        return  cost
    
    @property
    def instant_value(self):
        instant_value = self.number * self.current_price
        return  instant_value
    
    @property
    def profit_decoration(self):
        if self.instant_value < self.cost:
            return 'danger'
        else:
            return 'success'
        
    @property
    def profit(self):
        profit = self.instant_value - self.cost                    
        return profit

    @property
    def percentage(self):
        try:
            percentage = ((self.instant_value / self.cost) - 1) *100
        except ZeroDivisionError:
            percentage = 0
        return percentage
    
    @property
    def calculated_parities(self):
        currencies = Currency.objects.all()
        calculated_parities = {}
        for currency in currencies:
            curr = Currency.objects.get(currency_code = currency)
            rate = ExchangeRate.objects.get(
                from_currency_id=self.currency.pk, 
                to_currency_id = curr.pk).rate
            calculated_parities[curr.currency_code] = rate * self.instant_value
        return calculated_parities
    
    def __str__(self):
        return str(self.asset_type)
    
class AssetTimeData(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    price = models.FloatField()
    date = models.DateField()
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.category.name}-{self.currency.currency_code}-{self.date}"
    
