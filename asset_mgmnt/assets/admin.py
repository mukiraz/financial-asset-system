from django.contrib import admin

# Register your models here.

from .models import Category,Currency, UnitType, SwissStockHTMLContent, AssetType

# Register your models here.

admin.site.register(Category)
admin.site.register(Currency)
admin.site.register(UnitType)
admin.site.register(SwissStockHTMLContent)
admin.site.register(AssetType)
