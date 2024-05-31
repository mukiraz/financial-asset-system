import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from assets.models import Currency, ExchangeRate
from datetime import datetime

class Command(BaseCommand):
    help = 'Update currency exchange rates'

    def handle(self, *args, **kwargs):
        # Fetch all currency codes from the database
        currency_codes = Currency.objects.all()

        # API URL with your API key
        api_url = f'https://v6.exchangerate-api.com/v6/{settings.EXCHANGE_RATE_API_KEY}/latest/'

        # Fetch the latest exchange rates data from the API for all currency codes
        for currency in currency_codes:
            base_currency_code = currency.currency_code
            response = requests.get(api_url + base_currency_code)
            data = response.json()

            # Check if the request was successful
            if response.status_code == 200:
                try:
                    # Get the base currency
                    base_currency = Currency.objects.get(currency_code=base_currency_code)

                    # Iterate over the provided currency codes
                    for currency_code, rate in data['conversion_rates'].items():
                        # Skip the base currency
                        if currency_code == base_currency_code:
                            continue

                        try:
                            # Get the currency object from the database
                            to_currency = Currency.objects.get(currency_code=currency_code)

                            # Create or update ExchangeRate object for base currency to current currency
                            exchange_rate, created = ExchangeRate.objects.update_or_create(
                                from_currency_id=base_currency,
                                to_currency_id=to_currency,
                                defaults={'rate': rate, 'rate_date': datetime.now()}
                            )

                            self.stdout.write(self.style.SUCCESS(f'Exchange rate updated for {base_currency_code} to {currency_code}: {rate}'))

                            # Create or update ExchangeRate object for current currency to base currency
                            inverse_rate = 1 / rate
                            exchange_rate, created = ExchangeRate.objects.update_or_create(
                                from_currency_id=to_currency,
                                to_currency_id=base_currency,
                                defaults={'rate': inverse_rate, 'rate_date': datetime.now()}
                            )

                            self.stdout.write(self.style.SUCCESS(f'Exchange rate updated for {currency_code} to {base_currency_code}: {inverse_rate}'))

                        except Currency.DoesNotExist:
                            # Currency not found in the database
                            self.stdout.write(self.style.WARNING(f'Currency {currency_code} not found in the database'))

                except Currency.DoesNotExist:
                    # Base currency not found in the database
                    self.stdout.write(self.style.WARNING(f'Base currency {base_currency_code} not found in the database'))

            else:
                self.stdout.write(self.style.ERROR(f'Failed to fetch exchange rates for {base_currency_code}: {response.status_code} - {response.reason}'))

        for currency in currency_codes:
            currency_code = currency.currency_code
            currency = Currency.objects.get(currency_code=currency_code)

            exchange_rate, created = ExchangeRate.objects.update_or_create(
                                from_currency_id=currency,
                                to_currency_id=currency,
                                defaults={'rate': 1, 'rate_date': datetime.now()}
                            )
            self.stdout.write(self.style.SUCCESS(f'Exchange rate updated for {currency} to {currency}: {1}'))

        self.stdout.write(self.style.SUCCESS('All exchange rates updated successfully'))
