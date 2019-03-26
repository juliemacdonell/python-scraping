from urllib.request import urlopen
from bs4 import BeautifulSoup

url = 'https://www.mphil.de/en/calendar.html'
html = urlopen(url)
bs = BeautifulSoup(html, "html.parser")


def main():
    for child in bs.find('div', {'id': 'listview'}).children:
        print('-----------------------------------------------------')
        title = get_title(child)
        if title:
            print(title)


def get_title(child):
    try:
        attrs = child.a.img.attrs
    except AttributeError:
        return None

    return attrs.get('title')


if __name__ == '__main__':
    main()
