from django.contrib import admin

# Register your models here.

from .models import Category,Currency, UnitType, SwissStockHTMLContent, AssetType, Account, ExchangeRate, Asset

# Register your models here.

admin.site.register(Category)
admin.site.register(Currency)
admin.site.register(UnitType)
admin.site.register(SwissStockHTMLContent)
admin.site.register(AssetType)
admin.site.register(Account)
admin.site.register(ExchangeRate)
admin.site.register(Asset)
