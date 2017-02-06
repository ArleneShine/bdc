# -*- coding: utf-8 -*-
import requests
import re
from pyquery import PyQuery as pq


def get_index_html():
    url = "http://urbanlegends.about.com/"
    r = requests.get(url)
    with open('index.html', 'w') as f:
        f.write(r.text)


def get_class(url):
    part = re.match(r'http[s]*://urbanlegends.about.com/od/\S+', url)
    if part:
        part = re.match(r'http[s]*://urbanlegends.about.com/od/[^/\s]+/', url)
        del_part = re.match(r'http[s]*://urbanlegends.about.com/od/', url).group()
        if part:
            part = part.group()
            cla = part.replace(del_part, '').replace('/', '')
        else:
            cla = url.replace(del_part, '')
        return cla
    else:
        return ''


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
            cla = get_class(href)
            new.write('%s\t%s\t%s\n' % (title.encode('utf-8'), href.encode('utf-8'), cla.encode('utf-8')))


if __name__ == "__main__":
    get_categories()

