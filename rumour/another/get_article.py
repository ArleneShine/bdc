# -*- coding: utf-8 -*-

import glob
import requests
from pyquery import PyQuery as pq

catalog_path = 'catalog/'
article_url_path = 'article_url/'


def get_catalog():
    with open('category_url.tsv', 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            url = line[1]
            r = requests.get(url)
            html = r.text
            print line[0]
            with open('%s%s.html' % (catalog_path, line[0].replace('/', '-')), 'w') as new:
                new.write(html)


def get_article_url(html, filename):
    print "%s start" % filename
    doc = pq(html)
    divs1 = doc('div[class="article-unit article-unit-img-wrapper group"]')
    divs2 = doc('div[class="article-unit group"]')
    divs = [divs1, divs2]
    count = 0
    with open(filename, 'w') as f:
        for divs_ in divs:
            for div in divs_:
                div = pq(div)
                div1 = div('div[class="article-unit-desc"]')
                h5 = div1('h5[class="heading slab-heading"]')
                a = h5('a')
                if a:
                    title = a.text().replace('\t', '').replace('\n', '')
                    href = a.attr('href').replace('\t', '').replace('\n', '')
                    f.write('%s\t%s\n' % (title, href))
                    count += 1
    print ">>>>>>> %s contain %d" % (filename, count)
    return count


def get_all_article_url():
    index = 0
    for filename in glob.glob(r'%s*.html' % catalog_path):
        with open(filename, 'r') as f:
            html = f.read()
            count = get_article_url(html, filename.replace(catalog_path, article_url_path).replace('.html', '.tsv'))
            index += count
    print index


if __name__ == "__main__":
    get_all_article_url()
