from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from assets.models import AssetTimeData, Category, Currency, Asset
from assets.views import BaseTemplateObjects

class Command(BaseCommand):
    help = 'This command updates the categories and their total prices'

    def handle(self, *args, **kwargs):
        parity_calculator = BaseTemplateObjects().get_total_calculated_parities
        categories = Category.objects.all()
        currencies = Currency.objects.all()
        now = datetime.now()

        def insert_asset_data(category, total_prices):
            for currency in currencies:
                price = total_prices.get(currency.currency_code, 0)
                asset_time_data = AssetTimeData(
                    category=category,
                    currency=currency,
                    price=price,
                    date=now
                )
                asset_time_data.save()

        for category in categories:
            total_prices = {currency.currency_code: 0 for currency in currencies}
            filtered_assets = Asset.objects.filter(asset_type__category__pk=category.pk)
            
            if filtered_assets.exists():
                for asset in filtered_assets:
                    calculated_parities = parity_calculator([asset])
                    for currency_code, price in calculated_parities.items():
                        total_prices[currency_code] += price
            
            insert_asset_data(category, total_prices)

