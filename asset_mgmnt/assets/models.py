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
