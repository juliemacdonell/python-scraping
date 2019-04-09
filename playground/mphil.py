
from urllib.request import urlopen
import datetime as _dt

from bs4 import BeautifulSoup

url = 'https://www.mphil.de/en/calendar.html'
html = urlopen(url)
bs = BeautifulSoup(html, "html.parser")


def main():
    for child in bs.find('div', {'id': 'listview'}).children:
        if not child or (isinstance(child, str) and not child.strip()):
            continue

        # print(child)
        try:
            datetime = get_datetime(child)
            if datetime:
                formatted = datetime.strftime(
                    '%I:%M %p on %A, %B %D, %Y'
                ).lstrip('0')
                print(f'Date: {formatted}')

            composers = get_composers(child)
            if composers:
                print(f'Composers: {", ".join(composers)}')

            artists = get_artists(child)
            if artists:
                print(f'Artists: {", ".join(artists)}')

            print('-----------------------------------------------------')
        except Exception as exc:
            print(f'\t{exc}')
            print(f'\t{child}')
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
        hour_minute = time_.split()[0].split('_')
        hour = int(hour_minute[0])
        try:
            minute = int(hour_minute[1])
        except IndexError:
            minute = 0

        if 'p.m.' in time_:
            hour += 12

    return _dt.datetime(split[2], split[1], split[0], hour=hour, minute=minute)


def get_composers(child):
    try:
        composers = child.find('div', {'class': 'mp_popkomp'}).text
    except AttributeError:
        return None
    except TypeError:
        return None

    return composers.split()


def get_artists(child):
    try:
        artists = child.find('div', {'class': 'mp_popbesetzung'}).text
    except AttributeError:
        return None
    except TypeError:
        return None

    return [artist.replace(',', '') for artist in artists.split()]


if __name__ == '__main__':
    main()
