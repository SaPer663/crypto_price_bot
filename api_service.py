import requests
from config import end_point_api


def get_json_from_server(url_tail, url_base=end_point_api):
    url = url_base + url_tail
    try:
        return requests.get(url).json()
    except Exception as ex:
        return ex
