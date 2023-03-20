#import dependencies
import requests
# pull in api keys from config file
from config import public_key, private_key
# construct api request
response = requests.post(
    "https://api.tcgplayer.com/token",

    headers={
        "Content-Type": "application/json",
        "Accept": "application/json"},

    data=(f"grant_type=client_credentials"
          f"&client_id={public_key}&"
          f"client_secret={private_key}")
)
access = response.json()['access_token']
headers = {"accept": "application/json",
           "Content-Type": "application/json",
           'User-Agent': 'YOUR_USER_AGENT',
           "Authorization": "bearer " + access}
url = "https://api.tcgplayer.com/catalog/categories"
response = requests.get(url, headers=headers)
print(response.json())
url = "https://api.tcgplayer.com/catalog/categories/1/search"
payload = {"sort": "Relevance",
           "filters": [{
               "values": ["Tithe"],
               "name": "productName"
           }]}
search_response = requests.request("POST", url, json=payload, headers=headers)
print(search_response.json())
endpoint = "https://api.tcgplayer.com/catalog/products/"
productids = str(search_response.json()["results"])
url = endpoint + productids
response = requests.get(url, headers=headers)
response.json()
