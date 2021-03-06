# coding: utf-8
import requests
import json
import os

# supported_functions = ['TIME_SERIES_INTRADAY', 'TIME_SERIES_DAILY', 'TIME_SERIES_DAILY_ADJUSTED', 'TIME_SERIES_WEEKLY', 'TIME_SERIES_WEEKLY_ADJUSTED', 'TIME_SERIES_MONTHLY', 'TIME_SERIES_MONTHLY_ADJUSTED', 'GLOBAL_QUOTE', 'SYMBOL_SEARCH', 'CURRENCY_EXCHANGE_RATE', 'FX_INTRADAY', 'FX_DAILY', 'FX_WEEKLY', 'FX_MONTHLY', 'DIGITAL_CURRENCY_DAILY', 'DIGITAL_CURRENCY_WEEKLY', 'DIGITAL_CURRENCY_MONTHLY', 'SMA', 'EMA', 'WMA', 'DEMA', 'TEMA', 'TRIMA', 'KAMA', 'MAMA', 'VWAP', 'T3', 'MACD', 'MACDEXT', 'STOCH', 'STOCHF', 'RSI', 'STOCHRSI', 'WILLR', 'ADX', 'ADXR', 'APO', 'PPO', 'MOM', 'BOP', 'CCI', 'CMO', 'ROC', 'ROCR', 'AROON', 'AROONOSC', 'MFI', 'TRIX', 'ULTOSC', 'DX', 'MINUS_DI', 'PLUS_DI', 'MINUS_DM', 'PLUS_DM', 'BBANDS', 'MIDPOINT', 'MIDPRICE', 'SAR', 'TRANGE', 'ATR', 'NATR', 'AD', 'ADOSC', 'OBV', 'HT_TRENDLINE', 'HT_SINE', 'HT_TRENDMODE', 'HT_DCPERIOD', 'HT_DCPHASE', 'HT_PHASOR', 'SECTOR']
# be sure to update this when new parameters in Alpha Vantage are created
supported_endpoints = ['function', 'interval', 'symbol', 'outputsize', 'datatype', 'apikey', 'keywords', 'from_currency', 'to_currency', 'from_symbol', 'to_symbol', 'market', 'time_period', 'series_type', 'fast_limit', 'slow_limit', 'fastperiod', 'slowperiod', 'signalperiod', 'fastmatype',
                       'slowmatype', 'signalmatype', 'fastkperiod', 'slowkperiod', 'slowdperiod', 'slowkmatype', 'slowdmatype', 'fastdperiod', 'fastdmatype', 'fastdperiod', 'fastdmatype', 'matype', 'fast_period', 'slow_period', 'timeperiod1', 'timeperiod2', 'timeperiod3', 'nbdevup', 'nbdevdn', 'acceleration', 'maximum']

api_key = os.getenv("ALPHAVANTAGE_API_KEY")
_API_URL_PREFIX = "https://www.alphavantage.co/query?function="


def lambda_handler(event, context):
    result = handler(event)
    return result


def gcs_handler(request):
    av_data = request.json
    result = handler(av_data)
    return json.dumps(result)


def handler(av_request_data):
    if 'data' not in av_request_data:
        av_request_data['data'] = {}
    if 'id' not in av_request_data:
        av_request_data['id'] = ""

    query_url = create_api_url(av_request_data['data'])

    response = requests.get(query_url)
    error_string = None
    json_response = response.json()

    if not json_response:
        error_string = 'Error getting data from the api, no return was given.'
    elif "Error Message" in json_response:
        error_string = json_response["Error Message"]
    elif "Information" in json_response:
        error_string = json_response["Information"]
    elif "Note" in json_response:
        error_string = json_response["Note"]

    adapter_result = {'jobRunID': av_request_data['id'],
                      'data': json_response,
                      'status': str(response.status_code)}

    if error_string is not None:
        adapter_result['error'] = error_string
    return adapter_result


def create_api_url(data):

    url = ""
    url += _API_URL_PREFIX

    for k, v in data.items():
        if k in supported_endpoints and isinstance(k, str) and isinstance(v, str):
            url = url + "&" + k + "=" + v
    return url + "&apikey=" + api_key
    # return url.replace("datatype=csv", "")
