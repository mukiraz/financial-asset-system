import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus

url = 'https://apigw.vakifbank.com.tr:8443/getBISTPrices'
queryParams = '?' + urlencode({quote_plus('apikey'): 'l7xx5fe0fce1d27b4c20a679c73990089ee5'})
values = json.dumps({"SessionDate": "2024-06-05T00:00:00+03:00"}).encode('utf-8')
headers = {'Content-Type': 'application/json'}

request = Request(url + queryParams, data=values, headers=headers, method='POST')
response_body = urlopen(request).read()

print(response_body.decode('utf-8'))
