
from urllib.request import urlopen
import datetime as _dt

from bs4 import BeautifulSoup

url = 'https://www.mphil.de/en/calendar.html'
html = urlopen(url)
bs = BeautifulSoup(html, "html.parser")


def main():
    for child in bs.find('div', {'id': 'listview'}).children:
        datetime = get_datetime(child)
        if datetime:
            print(child)
            print(datetime)
            print('-----------------------------------------------------')



# def get_title(child):
#     try:
#         attrs = child.a.img.attrs
#     except AttributeError:
#         return None
#
#     return attrs.get('title')


def get_datetime(child):
    try:
        date = child.find('div', {'class': 'cal_date_date'}).text
    except AttributeError:
        return None
    except TypeError:
        return None

    try:
        time_ = child.find('div', {'class': 'cal_date_time'}).text
    except AttributeError:
        time_ = None

    split = [int(item) for item in date.split('_')]
    if time_ is None:
        hour = 0
    else:
        hour = int(time_.split()[0])
        if 'p.m.' in time_:
            hour += 12

    return _dt.datetime(split[2], split[1], split[0], hour=hour)


if __name__ == '__main__':
    main()
