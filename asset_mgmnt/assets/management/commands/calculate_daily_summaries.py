from django.core.management.base import BaseCommand
from django.utils import timezone
from assets.models import Asset, DailySummary, Currency
from assets.views import BaseTemplateObjects

class Command(BaseCommand):
    help = 'Calculate daily summaries for assets'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        assets = Asset.objects.select_related('asset_type', 'currency', 'asset_type__category').all()
        currencies = Currency.objects.all()
        
        liquid_assets = [asset for asset in assets if asset.asset_type.category.is_liquid]
        non_liquid_assets = [asset for asset in assets if not asset.asset_type.category.is_liquid]

        base_template = BaseTemplateObjects()


        all_parities = base_template.get_total_calculated_parities(assets)
        liquid_parities = base_template.get_total_calculated_parities(liquid_assets)
        non_liquid_parities = base_template.get_total_calculated_parities(non_liquid_assets)
        
        summaries = []
        for currency in currencies:
            summaries.append(DailySummary(
                date=today,
                currency=currency.currency_code,
                is_liquid=True,
                total_value=liquid_parities.get(currency.currency_code, 0)
            ))
            summaries.append(DailySummary(
                date=today,
                currency=currency.currency_code,
                is_liquid=False,
                total_value=non_liquid_parities.get(currency.currency_code, 0)
            ))
            summaries.append(DailySummary(
                date=today,
                currency=currency.currency_code,
                is_liquid=None,
                total_value=all_parities.get(currency.currency_code, 0)
            ))
        
        DailySummary.objects.bulk_create(summaries)
        self.stdout.write(self.style.SUCCESS('Successfully calculated and recorded daily summaries'))