import requests
from requests.auth import HTTPBasicAuth
import credentials


consumer_key = credentials.consumer_key
consumer_secret = credentials.consumer_secret
api_URL = (
    "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials")
r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
print(r.json())
json_response = r.json()

my_access_token = json_response['access_token']
