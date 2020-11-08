import json
from config import path


PATH = path

def read_file():
    try:
        with open(PATH) as file:
            return json.load(file)
    except Exception as ex:
        return str(ex)

def write_file(write_object):
    try:
        with open(PATH, 'w') as file:
            json.dump(write_object, file)
            return 0
    except Exception as ex:
        return str(ex)

def convert_json_to_daily_message(data_json, currency_name):
    currency_data = data_json
    message = f'{currency_name}:\n цена: {currency_data["data"]["last"]}\n\
         max: {currency_data["data"]["high"]}\n min: {currency_data["data"]["low"]}'
    return message

def convert_json_to_warning_message(current_price_value, last_price_value, currency_name):
    message = f'{currency_name}:\n большая волотильность\n\
         цена изменилась на {last_price_value - current_price_value}\n\
             текущая цена {current_price_value}'
    return message         