from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from assets.models import AssetTimeData, Category, Currency, Asset
from assets.views import BaseTemplateObjects

class Command(BaseCommand):
    help = 'This command updates the categories and their total prices'

    def handle(self, *args, **kwargs):
        parity_calculator = BaseTemplateObjects().get_total_calculated_parities
        categories = Category.objects.all()
        now = datetime.now()
        def insert_asset_data(asset):
            calculated_parities = parity_calculator(asset)
            for currency, price in calculated_parities.items():
                currency_obj = Currency.objects.get(currency_code=currency)
                asset_time_data = AssetTimeData(category = category,
                                                currency = currency_obj,
                                                price= price,
                                                date= now
                                                )
                asset_time_data.save()
        
        for category in categories:
            filtered_assets = Asset.objects.filter(asset_type__category__pk = category.pk)
            insert_asset_data(filtered_assets)            
            
            