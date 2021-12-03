from bs4 import BeautifulSoup as bs
import requests
from slugify import slugify
from mainapp.models import Notebooks

#сайт с которого паршу:https://nsv.by/catalog/kompyutery/


def parsing_one_page(URL):
    html = requests.get(URL)
    inf = {}
    soup = bs(html.content, "html.parser")
    inf['price'] = soup.find('span', 'price_value').text
    title = soup.find(id='pagetitle').text
    inf['title'] = title
    inf['slug'] = slugify(title)
    img = soup.find(id='photo-0')
    inf['img_src'] = img.find('img').attrs['src']
    return inf


def parse_links():
    URL = 'https://nsv.by/catalog/kompyutery/noutbuki/'
    html = requests.get(URL)
    soup = bs(html.content, "html.parser")

    links = soup.find_all(class_='dark_link js-detail-link')
    hrefs = []
    for href in links:
        hrefs.append(f"https://nsv.by{href['href']}")

    inf = []
    for href_ in hrefs:
        inf.append(parsing_one_page(href_))
    for href_ in inf:
        note = Notebooks.objects.create(slug=href_['slug'], title=href_['title'], price=href_['price'])
