# Financial Asset Management Software

## Introduction

Welcome to the Financial Asset Management Software! This application allows users to manage their financial assets, including gold, stock market investments, silver, funds, and more. The software calculates the total current value of the assets, generates informative graphics, and provides updates with the latest prices of various assets and currencies.

## Features

- **Asset Management**: Add and manage various financial assets including gold, stocks, silver, and funds.
- **Real-time Price Updates**: Fetch the latest price data for assets such as stocks and gold.
- **Currency Updates**: Calculate asset values with updated currency exchange rates.
- **Data Visualization**: Generate graphical representations of asset distributions and trends.
- **Detailed Reports**: Produce detailed reports and summaries of your financial assets.

## Installation
### Clone repository

`git clone https://github.com/mukiraz/financial-asset-system.git`

`cd financial-asset-system/`
`cd asset_mgmt/`

The application connects to https://www.exchangerate-api.com/ and fetches the parity data daily. You should sign up and get an api-key.
The api-key will be hold in .env file.

### Create an .env file

`touch .env`
open with nano editor.
`nano .env`

inside the .env file write this key-value pairs with your api key.

EXCHANGE_RATE_API_KEY={your api key}

Save the .env file and exit from nano editor.

### Create a virtual environment
`python3 -m venv ./asset-mgmnt-env`

Activate it

`source asset-mgmt-env/bin/activate`

### Install python packages
`pip3 install -r requirements.txt`

### IP Configuration

`cd asset_mngmnt/asset_mngmnt/`

`nano settings.py`

find the ALLOWED_HOSTS variable and write your IP address. To find your IP address you can use ifconfig

ALLOWED_HOSTS = ['{your-host-ip-here}','localhost']

Save the settings.py file and exit from nano editor.

### Creating Database

Go to
`~/financial-asset-management/asset_mgmt/` folder.

Run these commands:

`python manage.py makemigrations`
`python manage.py migrate`

### Fetching Data

#### Fetching Currencies from https://www.exchangerate-api.com/

Run this command to fetch current exchange rates.

`python3 manage.py update_currencies`

#### Fetching updatable Asset Types.

Asset types are the stock names, gold, silver or other commodities. 

Run this command to get asset types.

`python3 manage.py update_asset_types`

All asset types are updated approximately 20 mins.

##### Commodity

For gold, silver or other commodities, the applicatin connects to:

https://uzmanpara.milliyet.com.tr/altin-fiyatlari/

and fetches the data.

##### BIST100

For Borsa Istanbul stocks, the application connects to:

https://www.getmidas.com/canli-borsa/

and fetches the data.

##### For Swiss stock market

This is a non profit and low cost application. Hence, the swiss stock data fetched from

https://www.investing.com/equities/switzerland

web page. The html content does not fetched from directly web page. The html content is obtained 
from the web page source manually and inserted into database to the "Swiss_stock_html_content"
table.

Fetching data period is aproximately 20 minutes :(

##### Crypto Assets

Crypto assets are fetched from binance crypto stock market wit an API.

You don't need a cryptographic authentication to reach binance API.

### Adding Crontab.

The application updates the currency exchange rates, asset types, daily asset summary, daily asset time data.

In order to automatize it create crontab.

`crontab -e`

paste this scripts fo file and save it.

paste full path of the "financial-asset-system" folder!


5 8-20 * * * /usr/bin/python ~/financial-asset-system/asset_mgmt/manage.py update_asset_types
30 20 * * * /usr/bin/python ~/financial-asset-system/asset_mgmt/manage.py update_asset_time_data
0 8 * * * /usr/bin/python ~/financial-asset-system/asset_mgmt/manage.py update_currencies
35 20 * * * /usr/bin/python ~/financial-asset-system/asset_mgmt/manage.py calculate_daily_summaries


### Reaching the web page

open a browser and go to the server IP address:

http://{server ip address}:8000/


## Prerequisites

- Python 3.6+
- Django 3.2+
- Virtual Environment tool (optional but recommended)

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
Thank you to all the contributors who helped in developing this project.
Special thanks to the open-source community for providing various tools and libraries that made this project possible.

## Contact
For any questions or suggestions, please open an issue or contact us at mukiraz@mukiraz.com