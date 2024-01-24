import time
import requests
from datetime import datetime

def check_post(track):
    session = requests.session()

    response = session.get(f'https://moyaposylka.ru/api/v1/carriers/{track}')
    mail_sender = response.json()[0]['code']

    response = session.post(f'https://moyaposylka.ru/api/v1/trackers/{mail_sender}/{track}/realtime')
    for i in range(20):
        response = session.get(f'https://moyaposylka.ru/api/v1/trackers/{mail_sender}/{track}/realtime')
        if response.status_code == 200:
            return response.json()
        time.sleep(1)
    return 'error'

def parse_post(jsn: dict):

    res = jsn['events'][0]
    res['eventDate'] = datetime.fromtimestamp(res['eventDate']//1000).strftime('%d.%m.%Y %H:%M:%S')
    return res


# track = 'RLBQ00089378'
# # eventDate
# # operation
# # location
# print(parse_post(check_post(track)))
    # events[0].location
