from django.core.management.base import BaseCommand
from assets.api_integration import Commodity, BIST100, SwissStock, CryptoCurrency
from assets.models import AssetType, Category, SwissStockHTMLContent

class Command(BaseCommand):
    help = 'This command updates the asset types'

    def handle(self, *args, **kwargs):
        commodity = Commodity("https://uzmanpara.milliyet.com.tr/altin-fiyatlari/")
        bist_100 = BIST100("https://www.getmidas.com/canli-borsa/")
        html_content = SwissStockHTMLContent.objects.get(pk=1)
        swiss_stock = SwissStock(html_content.html_content, get_cotent_from_database = True)
        crypto_asset = CryptoCurrency()


        df_gold = commodity.get_gold_df()
        df_commodity = commodity.get_commodity_df()
        df_silver = commodity.get_silver_df()
        df_bist_100 = bist_100.get_stocks()
        df_swiss_stock = swiss_stock.get_stocks()
        df_crypto_names_and_prices = crypto_asset.get_crypto_names_and_prices()

        asset_types = {
            'Altın': df_gold,
            'Gümüş': df_silver,
            'Emtia': df_commodity,
            'BIST100': df_bist_100,
            'İsviçre Borsası':df_swiss_stock,
            'Kripto Varlık':df_crypto_names_and_prices
        }

        for asset_name, df in asset_types.items():
            category = Category.objects.get(name=asset_name)
            print(f"Updating {category.name}")         
            for index, row in df.iterrows():
                name = row["name"]
                current_price = row['current_price']
                asset_type, created = AssetType.objects.get_or_create(name=name, 
                                                                      category=category, 
                                                                      defaults={
                                                                          'current_price':current_price
                                                                      })
                asset_type.current_price = current_price
                asset_type.save()
        print("Update finished")
        



