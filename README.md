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

`git clone https://github.com/mukiraz/financial-asset-management.git`

`cd financial-asset-management/`
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

### Creating Database

`cd asset_mgmt/asset_mgmt/`

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
`python manage.py runserver 0.0.0.0:8000`

### Reaching the web page

open a browser and go to the server IP address:

http://{server ip address}:8000/




### Prerequisites

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