import requests
import os 
import logging
import datetime 
from datetime import date, timedelta


# from model import forecast

URL_CAREGORIES = "categories"
URL_SALES = "sales"
URL_STORES = "shops"
URL_FORECAST = "forecast"

api_port = os.environ.get("API_PORT", "8000")
api_host = os.environ.get("API_PORT", "localhost")

_logger = logging.getLogger(__name__)
# Init the app
# app = Flask()

def get_address(resource):
    return "http://" + api_host + ':' + api_port + "/" + "resource"

def get_stores():
    stores_url = get_address(URL_STORES)
    resp = requests.get(stores_url)
    if resp.status_code != 200:
        _logger.warning("Could not get stores info")
        
    return resp.json()['data']

def get_categs_info():
    categs_url = get_address(URL_CAREGORIES)
    resp = requests.get(categs_url)
    if resp.status_code != 200:
        _logger.warning("Could not get category info")
        return {}
    result = {el['sku'] : el for el in resp.json()['data']}
    return result




def main(today=date.today()):
    forecast_dates = [today + timedelta(days=d) for d in range(1,6)]
    forecast_dates = [el.strftime("%Y-%m-%d") for el in forecast_dates]
    categs_info = get_categs_info()
    for store in get_stores():
        result = []















if __name__ == "__main__":
    main()