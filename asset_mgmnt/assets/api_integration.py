import requests, io, urllib.error, re, time, os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
from bs4 import BeautifulSoup
from binance.client import Client


class Asset():
    def __init__(self, url):
        self.url = url

    def fetch_data(self):
        try:
            return pd.read_html(self.url, encoding="utf-8")
        except urllib.error.HTTPError:
            header = {
                      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                      "X-Requested-With": "XMLHttpRequest"
                    }
            r = requests.get(self.url, headers=header)
            return pd.read_html(io.StringIO(r.text), encoding="utf-8")
        
    
    def rename_df_columns(self, df):
        first_column_name = df.columns[0]
        second_column_name = df.columns[1]
        new_columns = {
            first_column_name : 'name',
            second_column_name :'current_price'
        }
        return df.rename(columns=new_columns)
        
    
    def convert_price_to_numeric(self, df_list, numeric_column):
        for df in df_list:
            numeric_values = pd.to_numeric(df[numeric_column], errors='coerce')
            is_numeric = numeric_values.notna().all()
            if not is_numeric:
                df[numeric_column] = df[numeric_column].str.replace(' TL', '').str.replace('.', '').str.replace(',', '.')
                df[numeric_column] = pd.to_numeric(df[numeric_column], errors='coerce')
        return df_list
    
class Commodity(Asset):    
    def __init__(self, url):
        super().__init__(url)
        commodity_df_list = self.fetch_data()
        df_list = self.convert_price_to_numeric(commodity_df_list, "Alış")
        df_gold = df_list[0]
        df_silver = df_list[2]
        df_commodity = df_list[3]
        self.df_gold = df_gold[["Altın","Alış"]]
        self.df_silver = df_silver[["Gümüş","Alış"]]
        self.df_commodity = df_commodity[["Emtia","Alış"]]
        self.df_gold = self.rename_df_columns(self.df_gold)
        self.df_silver = self.rename_df_columns(self.df_silver)
        self.df_commodity = self.rename_df_columns(self.df_commodity)
        
    
    def get_gold_df(self):
        return self.df_gold
    
    def get_silver_df(self):
        self.df_silver["current_price"] = self.df_silver["current_price"] / 100
        return self.df_silver
    
    def get_commodity_df(self):
        return self.df_commodity
    
class BIST100(Asset):
    def __init__(self, url):        
        super().__init__(url)
        stocks_list = self.fetch_data()
        stocks_list['current_price'] = pd.to_numeric(stocks_list['current_price'], errors='coerce')
        self.stocks = stocks_list
        
        
    def fetch_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='stock-table w-100')

        # Initialize lists to store the data
        hisse_list = []
        son_list = []

        # Check if the table was found
        if table:
            # Find all rows in the tbody
            rows = table.find('tbody', class_='table-body').find_all('tr')

            for row in rows:
                # Get the "Hisse" column (first column)
                hisse = row.find('td', class_='val first').text.strip()

                # Get the second "td" element, which corresponds to the "Son" column
                son = row.find_all('td', class_='val')[1].text.strip()

                # Append the data to the lists
                hisse_list.append(hisse)
                son_list.append(son.replace(".","").replace(",","."))
        else:
            print('Table not found')

        df = pd.DataFrame({
            'name':hisse_list,
            'current_price':son_list
        })
        return df
    
    def get_stocks(self):
        return self.stocks
    
class SwissStock():
    def __init__(self, html_content, get_cotent_from_database = True):
        if get_cotent_from_database is True:
            self.html_content_table = html_content
        else:
            __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            full_path = os.path.join(__location__, 'swiss_market.html')
            self.html_content_table = open(full_path,"r")

    def get_stock_addresses(self):
        soup = BeautifulSoup(self.html_content_table, 'html.parser')
        target_links = soup.find_all("a", class_="text-ellipsis")
        hrefs = [link.get('href') for link in target_links]
        url_lists = []
        for href in hrefs:
            url_lists.append("https://www.investing.com"+href)
        return url_lists
    
    def get_stock_name_and_price(self):
        url_lists = self.get_stock_addresses()
        stock_names = []
        prices = []
        print("Fetching data started.")
        for url_list in url_lists:
            response = requests.get(url_list)
            time.sleep(1)
            # Get the HTML content of the webpage
            html_content = response.text
            
            # Parse HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            try:
                h1 = soup.find("h1", class_="font-bold")
                price = soup.find("div", attrs={"data-test":"instrument-price-last"}).get_text()
                price = float(price.replace(",",""))
                text= h1.text
                pattern = r'\((.*?)\)'
                matches = re.findall(pattern, text)
                if matches:
                    stock_name = matches[0]
                    stock_names.append(stock_name)
                    prices.append(price)
                    print(f'{stock_name} fetched with price: {price}')
                del(soup)
            except AttributeError:
                continue

        df_stock_names_and_prices = {
            "name": stock_names,
            "current_price":prices
        }
        
        return df_stock_names_and_prices
    def get_stocks(self):
        stocks = pd.DataFrame(self.get_stock_name_and_price())
        return stocks
    def __del__(self):
        try:
            self.html_content_table.close()
        except AttributeError:
            pass

class CryptoCurrency():
    def __init__(self, api_key="", api_secret=""):
        client = Client(api_key, api_secret)        
        prices = client.get_all_tickers()        
        df_crypto_names_and_prices = pd.DataFrame(prices)
        df_crypto_names_and_prices.columns = ['name', 'current_price']

        # Convert the price column to floats
        df_crypto_names_and_prices['current_price'] = df_crypto_names_and_prices['current_price'].astype(float)

        self.df_crypto_names_and_prices = df_crypto_names_and_prices
    
    def get_crypto_names_and_prices(self):
        return self.df_crypto_names_and_prices
    

bist_100 = BIST100("https://www.getmidas.com/canli-borsa/")

stocks = bist_100.get_stocks()

print(stocks)

