import json
import api_db as api
from time import sleep, localtime
from api_service import get_json_from_server
from config import first_pair, first_currency_name, second_pair, second_currency_name
from bot import send_message



first_pair_data = {}
first_pair_last_price = 0
second_pair_data = {}
second_pair_last_price = 0

def is_big_change(current_price, last_price):
    if abs(current_price - last_price) > 90:
        return True
    else:
        return False 

while True:
    first_pair_data = get_json_from_server(first_pair)
    second_pair_data = get_json_from_server(second_pair)
        
    first_pair_current_price = first_pair_data[0]['data']['last']
    second_pair_current_price = second_pair_data[1]['data']['last']
    if is_big_change(first_pair_current_price, first_pair_last_price):
        message = api.convert_json_to_warning_message(
            first_pair_current_price,
            first_pair_last_price,
            first_currency_name
        )
        send_message(message)

    if is_big_change(second_pair_current_price, second_pair_last_price):
        message = api.convert_json_to_warning_message(
            second_pair_current_price,
            second_pair_last_price,
            second_currency_name
        )
        send_message(message)
    first_pair_last_price = first_pair_current_price
    second_pair_last_price = second_pair_current_price

    api.write_file([first_pair_data, second_pair_data])
    if localtime().tm_hour == 10:
        send_message(api.convert_json_to_daily_message(first_pair_data, first_currency_name))
        send_message(api.convert_json_to_daily_message(second_pair_data, second_currency_name))
        
    sleep(900)

