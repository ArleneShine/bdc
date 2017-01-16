# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
import traceback
import glob
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

result_path = "result/"


def get_article_num(html):
    doc = pq(html)
    div = doc('div[class="widget page-btns-wrapper"]')
    divs1 = div('div[class="col col-1"]')
    lis = list()
    for div1 in divs1:
        div1 = pq(div1)
        a = div1('a')
        href = a.attr('href')
        num = a.text()
        if href:
            lis.append(num)
    index = 1
    if lis:
        for li in lis:
            if int(li) > index:
                index = int(li)
    return index


def get_content2(html):
    lis = list()
    doc = pq(html)
    div = doc('div[id="content"]')
    article = div('article[class="content widget widget-alt expert-content expert-content-text"]')
    ps = article.children('p')
    ps = ps('p')
    for p in ps:
        p = pq(p)
        lis.append(p.text())
    return lis


def get_content1(html):
    lis = list()
    doc = pq(html)
    divs = doc('div[class="expert-content-text"]')
    for div in divs:
        div = pq(div)
        ps = div.children()('p')
        for p in ps:
            p = pq(p)
            lis.append(p.text())
    return lis


def get_content3(html):
    lis = list()
    doc = pq(html)
    divs = doc('div[class="col-push-2 col-push-tablet-1 content-responsive"]')
    for div in divs:
        div = pq(div)
        ps = div.children()('p')
        for p in ps:
            p = pq(p)
            lis.append(p.text())
    return lis


def get_content4(html):
    lis = list()
    doc = pq(html)
    divs = doc('div[class="content content-list"]')
    for div in divs:
        div = pq(div)
        div = div.children()
        h2 = div('h2')
        lis.append(h2.text())
        divs1 = div('div[class="content-list-body"]')
        for div1 in divs1:
            div1 = pq(div1).children()
            ps = div1('p')
            for p in ps:
                p = pq(p)
                lis.append(p.text())
    return lis


def get_content5(html):
    lis = list()
    doc = pq(html)
    divs = doc('div[class="comp flex article-content"]')
    for div in divs:
        div = pq(div).children()
        ps = div('p')
        for p in ps:
            p = pq(p)
            lis.append(p.text())
    return lis


def get_content6(html):
    lis = list()
    doc = pq(html)
    divs = doc('div[id="articlebody"]')
    for div in divs:
        div = pq(div).children()
        ps = div('p')
        for p in ps:
            p = pq(p)
            lis.append(p.text())
    return lis


def get_date(html):
    doc = pq(html)
    date = doc('meta[itemprop="dateModified"]').attr('content')
    if date:
        date = date.replace('T', ' ').replace('.000Z', '').strip()
    else:
        s = re.search(r'"dateModified":[\s\t\r\n]*"\S+T\S+.000Z"', html)
        if s:
            s = s.group()
            part = re.match(r'dateModified":[\s\t\r\n]*"', s)
            if part:
                part = part.group()
                date = s.replace(part, "")
    return date


def get_title(html):
    doc = pq(html)
    div = doc('div[class="article-header article-header-full"]')
    h1 = div('h1')
    title = h1.text().strip()
    return title


def write_result(category, title, url, date, content):
    with open('%s%s.csv' % (result_path, category), 'a') as f:
        f.write('"%s","%s","%s","%s","%s"\n' % (title, url, date, content, category))


def clean_all_article():
    for filename in glob.glob(r'article_url/*.tsv'):
        print '------ %s start --------' % filename
        category = filename.replace('.tsv', '').replace('article_url/', '')
        with open('%s%s.csv' % (result_path, category), 'w') as f:
            f.write('"Title","Url","Date","Content","Category"\n')
        with open(filename, 'r') as f:
            for line in f:
                l = line.strip().split('\t')
                if len(l) == 2:
                    filename = 'html/%s/%s.html' % (
                        category.replace(' ', '_').replace('&', 'and').replace("'", '').replace('"', ''),
                        l[0].replace('/', '-').replace('.', '_'))
                    with open(filename, 'r') as f:
                        html = f.read()
                    lis = get_content1(html)
                    if not lis:
                        lis = get_content2(html)
                        if not lis:
                            lis = get_content3(html)
                            if not lis:
                                lis = get_content4(html)
                                if not lis:
                                    lis = get_content5(html)
                                    if not lis:
                                        lis = get_content6(html)
                    content_lis = [_ for _ in lis]
                    num = get_article_num(html)
                    title = get_title(html)
                    date = get_date(html)
                    if date is None:
                        date = ""
                        print '%s/%s' % (category, l[0])
                    if num >= 2:
                        for i in range(2, num + 1):
                            with open(filename.replace('html/', 'html1/').replace('.html', '%d.html' % i), 'r') as f1:
                                html1 = f1.read()
                                lis = get_content1(html1)
                                if not lis:
                                    lis = get_content2(html1)
                                    if not lis:
                                        lis = get_content3(html1)
                                        if not lis:
                                            lis = get_content4(html1)
                                            if not lis:
                                                lis = get_content5(html1)
                                                if not lis:
                                                    lis = get_content6(html1)
                                for li in lis:
                                    content_lis.append(li)
                    content = ""
                    if content_lis:
                        for li in content_lis:
                            content += '  %s\n' % li
                    else:
                        print '%s/%s >> %s' % (category, l[0], l[1])
                    with open('%s%s.csv' % (result_path, category), 'a') as f:
                        f.write('"%s","%s","%s","%s","%s"\n' % (title.encode("utf-8"), l[1].encode("utf-8"),
                                                                date.encode("utf-8"),
                                                                content.replace('"',"'").encode("utf-8"),
                                                                category.encode("utf-8")))
                else:
                    with open('error.csv', 'a') as error:
                        error.write(line)


if __name__ == "__main__":
    clean_all_article()

    '''
    with open('test.html', 'r') as f:
        html = f.read()
    get_content6(html)'''



