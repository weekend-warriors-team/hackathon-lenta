# import requests
# import pandas as pd
# import os 
# from datetime import date, timedelta
# from flask import Flask
from model import sales_submission_out

# api_host = os.environ.get("API_PORT", "8000")
# api_port = os.environ.get("API_PORT", "localhost")

# app = Flask(__name__)

sales_submission_out.to_csv('ds\sales_submission_out.csv')


if __name__ == "__main__":
    pass