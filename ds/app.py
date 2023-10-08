import requests
import pandas as pd
import os 
from datetime import date, timedelta
from flask import Flask
from model import sales_submission_out

api_host = os.environ.get("API_PORT", "8000")
api_port = os.environ.get("API_PORT", "localhost")

app = Flask(__name__)

list_data = ['pr_df', 'sales_df_train', 'st_df']
list_resource = []


def data(df):
    df = pd.read_csv(f'ds\\data\\{df}.csv')
    return f'{df}.csv'
# def main():
#     return

def get_adress(resource):
    return "http://" + api_host + ":" + api_port + "/" + resource
  
# def get_data(data, resource):
#     adress = get_adress(resource)
#     data = requests.get(adress)
#     if data.status_code != 200:
#         print("Could not requested resource")
#         return {}
#     data.to_csv(f'ds\data\{data}.csv')
#     return 
   
# def forecast(adress, sale_submission):
#     requests.post(adress, sale_submission)

for df in list_data:
    df = data(df)
    print(df)
    print(df)



# print(pr_df)
# forecast(get_adress(resource), sales_submission_out)

if __name__ == "__main__":
    data(df)