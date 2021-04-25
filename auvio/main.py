import requests
from bs4 import BeautifulSoup
import time
import re
import sys

s = requests.Session()


def logout():
    url = 'https://irs.zuvio.com.tw/student5/logout/index'
    s.get(url)


def check_roll_call(class_number: str):
    url = 'https://irs.zuvio.com.tw/student5/irs/rollcall/' + class_number
    result = s.get(url)
    result.encoding = 'big-5'
    if '簽到開放中' in result.text:
        return True
    else:
        return False


def get_information(class_number: str):
    url = 'https://irs.zuvio.com.tw/student5/irs/rollcall/' + class_number
    result = s.get(url)
    result.encoding = 'big-5'

    soup = BeautifulSoup(result.text, 'html.parser')
    pattern_user_id = re.compile(r"var user_id = (.+)[,;]")
    user_id = re.search('var user_id = (.+)[,;]', str(soup.find('script', text=pattern_user_id))).group(1)
    pattern_access_token = re.compile(r"var accessToken = (.+)[,;]")
    access_token = re.search('var accessToken = "(.+)"[,;]',
                             str(soup.find('script', text=pattern_access_token))).group(1)
    pattern_roll_call_id = re.compile(r"var rollcall_id = (.+)[,;]")
    roll_call_id = re.search('''var rollcall_id = '(.+)'[,;]''',
                             str(soup.find('script', text=pattern_roll_call_id))).group(1)

    return user_id, access_token, roll_call_id


def auto_roll_call(class_number: str, lat: float, lng: float):
    while True:
        try:
            if check_roll_call(class_number):
                url = 'https://irs.zuvio.com.tw/app_v2/makeRollcall'
                user_id, access_token, roll_call_id = get_information(class_number)
                data = {
                    'user_id': user_id,
                    'accessToken': access_token,
                    'rollcall_id': roll_call_id,
                    'device': 'WEB',
                    'lat': str(lat),
                    'lng': str(lng)
                }
                res = s.post(url, data=data)
                if b'"status":true' in res.content:
                    print('success')
            time.sleep(60)
        except KeyboardInterrupt:
            print('logout ...')
            try:
                logout()
                break
            except SystemExit:
                sys.exit(0)


def login(email: str, password: str) -> bool:
    url = 'https://irs.zuvio.com.tw/irs/submitLogin'
    data = {
        'email': email,
        'password': password,
        'current_language': 'zh-TW'
    }
    result = s.post(url, data=data)
    result.encoding = 'big-5'
    return not ('密碼錯誤' in result.text or '查無此電子郵件' in result.text)


def auvio(email: str, password: str, class_number: str, lat: float, lng: float):
    if not all((email, password, class_number, lat, lng)):
        raise Exception

    if not login(email, password):
        print('email or password is wrong')
    else:
        auto_roll_call(class_number, lat, lng)

