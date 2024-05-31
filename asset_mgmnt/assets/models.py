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
    
