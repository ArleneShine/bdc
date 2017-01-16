# -*- coding: utf-8 -*-
import requests
from pyquery import PyQuery as pq


def get_index_html():
    url = "http://urbanlegends.about.com/"
    r = requests.get(url)
    with open('index.html', 'w') as f:
        f.write(r.text)


def get_categories():
    with open('index.html', 'r') as f:
        html = f.read()
    doc = pq(html)
    div = doc('div[class="caret-list circ-list fixed widget full-length"]')
    ul = div('ul')
    lis = ul('li')
    with open('category_url.tsv', 'w') as new:
        for li in lis:
            li = pq(li)
            title = li('a').text().replace('\t', '').replace('\n', '')
            href = li('a').attr('href').replace('\t', '').replace('\n', '')
            new.write('%s\t%s\n' % (title, href))


if __name__ == "__main__":
    get_categories()

