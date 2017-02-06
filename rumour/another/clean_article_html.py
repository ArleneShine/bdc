# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
import datetime
import glob
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

result_path = "result/"


def get_category_url():
    urls = list()
    with open('category_url.tsv', 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            urls.append(line[1])
    return urls


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


def get_headline(html):
    doc = pq(html)
    div = doc('div[class="article-header article-header-full"]')
    h1 = div('h1')
    head = h1.text()
    if head == "":
        div = doc('div[class="header-title"]')
        head = div.text()
        if head == "":
            div = doc('div[id="articlebody"]')
            h1 = div('h1')
            head = h1.text()
            if head == "":
                div = doc('div[class="storyHead"]')
                h1 = div('h1')
                head = h1.text()
                if head == "":
                    div = doc('div[class="article-header article-header-mini"]')
                    h1 = div('h1')
                    head = h1.text()
                    if head == "":
                        div = doc('div[class="content-wrapper"]')
                        h1 = div('h1')
                        head = h1.text()
                        if head == "":
                            div = doc('div[id="content"]')
                            h1 = div('h1')
                            head = h1.text()
                            if head == "":
                                s = re.search(r'<!-- Write Headline Here -->[\s\S]+<!-- End of Headline -->', html)
                                if s:
                                    head = s.group().replace('<!-- Write Headline Here -->', '').replace(
                                        '<!-- End of Headline -->', '').strip()
                                else:
                                    return None
    return head.replace('"', "'")


# 0 : 488
def get_content0(html):
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


# 1 : 216
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


# 2 : 172
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


# 3 : 80
def get_content3(html):
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


# 4 : 13
def get_content4(html):
    lis = list()
    doc = pq(html)
    divs = doc('div[id="flex_1-0"]')
    for div in divs:
        div = pq(div).children()
        ps = div('p')
        for p in ps:
            p = pq(p)
            lis.append(p.text())
    return lis


# 5 : 7
def get_content5(html):
    lis = list()
    doc = pq(html)
    divs = doc('div[class="comp flex article-content expert-content"]')
    for div in divs:
        div = pq(div).children()
        ps = div('p')
        for p in ps:
            p = pq(p)
            lis.append(p.text())
    return lis


# 6 : 7
def get_content6(html):
    lis = list()
    doc = pq(html)
    divs = doc('div[class="comp flex article-content expert-content"]')
    for div in divs:
        div = pq(div).children()
        ps = div('p')
        for p in ps:
            p = pq(p)
            lis.append(p.text())
    return lis


# 7 : 4
def get_content7(html):
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


# 8
def get_content8(html):
    lis = list()
    doc = pq(html)
    divs = doc('div[class="transcript-body expert-content"]')
    for div in divs:
        div = pq(div)
        div = div.children()
        ps = div('p')
        for p in ps:
            p = pq(p)
            lis.append(p.text())
    return lis


# 9
def get_content9(html):
    lis = list()
    doc = pq(html)
    divs = doc('div[id="mainBodyArea"]')
    for div in divs:
        div = pq(div)
        ps = div('p')
        for p in ps:
            p = pq(p)
            lis.append(p.text())
    return lis


# 10
def get_content10(html):
    lis = list()
    doc = pq(html)
    divs = doc('div[class="article-text"]')
    for div in divs:
        div = pq(div)
        div = div.contents()
        for d in div:
            if not re.match(r'[\s\t\r\n]*$', str(d)):
                d = pq(d)
                if not d.find('script'):
                    text = d.text()
                    if not re.match(r'[\s\t\r\n]*$', text):
                        lis.append(text)
    return lis


# 11
def get_content11(html):
    lis = list()
    doc = pq(html)
    divs = doc('div[class="intro expert-content-text"]')
    for div in divs:
        div = pq(div)
        div = div.contents()
        for d in div:
            if not re.match(r'[\s\t\r\n]*$', str(d)):
                d = pq(d)
                if not d.find('script'):
                    text = d.text()
                    if not re.match(r'[\s\t\r\n]*$', text):
                        lis.append(text)
    return lis


# 12
def get_content12(html):
    lis = list()
    doc = pq(html)
    divs = doc('div[id="content"]')
    for div in divs:
        div = pq(div)
        div = div.contents()
        for d in div:
            if not re.match(r'[\s\t\r\n]*$', str(d)):
                d = pq(d)
                if not d.find('script') and not d.find('h1'):
                    text = d.text()
                    if not re.match(r'[\s\t\r\n]*$', text):
                        lis.append(text)
    return lis


def get_date(html):
    doc = pq(html)
    date = doc('meta[itemprop="datePublished"]').attr('content')
    if date:
        date = date.replace('T', ' ').replace('.000Z', '').strip()
    else:
        s = re.search(r'"datePublished":[\s\t\r\n]*"\S+T\S+.000Z"', html)  # "dateModified": "2016-10-19T23:09:07.000Z"
        if s:
            s = s.group()
            part = re.match(r'"datePublished":[\s\t\r\n]*"', s)
            if part:
                part = part.group()
                date = s.replace(part, "").replace('T', ' ').replace('.000Z"', '').strip()
        else:
            date = doc('meta[name="pd"]').attr('content')
            if date:
                date = date.replace(' UTC', '')
                try:
                    date = str(datetime.datetime.strptime(date, '%A, %d-%b-%Y %H:%M:%S'))
                except:
                    print date
                    return None
    return date


def delete_blank_line(content):
    lines = re.findall(r'\n[\s\t\r\n]*\n', content)
    for line in lines:
        content = content.replace(line, '\n')
    return content


def write_result(category, title, url, date, content):
    with open('%s%s.csv' % (result_path, category), 'a') as f:
        f.write('"%s","%s","%s","%s","%s"\n' % (title, url, date, content, category))


def clean_all_article():
    count = 0
    parse_count = 0
    date_count = 0
    head_count = 0
    # category_url = get_category_url()
    for filename in glob.glob(r'article_url/*.tsv'):
        print '------ %s start --------' % filename
        category = filename.replace('.tsv', '').replace('article_url/', '')
        with open('%s%s.csv' % (result_path, category), 'w') as f:
            f.write('"Title","Url","Article-title","Date","Content","Category","class"\n')
        with open(filename, 'r') as f:
            for line in f:
                count += 1
                l = line.strip().split('\t')
                if len(l) == 3:
                    filename = 'html/%s/%s.html' % (
                        category.replace(' ', '_').replace('&', 'and').replace("'", '').replace('"', ''),
                        l[0].replace('/', '-').replace('.', '_'))
                    with open(filename, 'r') as f:
                        html = f.read()
                    lis = get_content0(html)
                    if not lis:
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
                                            if not lis:
                                                lis = get_content7(html)
                                                if not lis:
                                                    lis = get_content8(html)
                                                    if not lis:
                                                        lis = get_content9(html)
                                                        if not lis:
                                                            lis = get_content10(html)
                                                            if not lis:
                                                                lis = get_content11(html)
                                                                if not lis:
                                                                    lis = get_content12(html)
                    content_lis = [_ for _ in lis]
                    num = get_article_num(html)
                    if num >= 2:
                        for i in range(2, num + 1):
                            with open(filename.replace('html/', 'html1/').replace('.html', '%d.html' % i), 'r') as f1:
                                html1 = f1.read()
                                lis = get_content0(html1)
                                if not lis:
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
                                                        if not lis:
                                                            lis = get_content7(html1)
                                                            if not lis:
                                                                lis = get_content8(html1)
                                                                if not lis:
                                                                    lis = get_content9(html1)
                                                                    if not lis:
                                                                        lis = get_content10(html1)
                                                                        if not lis:
                                                                            lis = get_content11(html1)
                                                                            if not lis:
                                                                                lis = get_content12(html)
                                for li in lis:
                                    content_lis.append(li)
                    content = ""
                    if content_lis:
                        for li in content_lis:
                            content += '  %s\n' % li
                        content = delete_blank_line(content)
                    else:
                        parse_count += 1
                        with open('no_content.csv', 'a') as new:
                            new.write('%s\t%s\n' % (l[0], l[1]))
                        print 'content -> %s/%s >> %s == file:///home/dundun/桌面/rumour/another/%s' % (category, l[0], l[1], filename)
                        continue
                    title = l[0].replace('"', "'")
                    date = get_date(html)
                    head = get_headline(html)
                    if head is None:
                        head = ""
                        head_count += 1
                        with open('no_title.csv', 'a') as new:
                            new.write('%s\t%s\n' % (l[0], l[1]))
                        print 'head -> %s/%s >> %s == file:///home/dundun/桌面/rumour/another/%s' % (category, l[0], l[1], filename)
                    if date is None:
                        date = ""
                        date_count += 1
                        with open('no_date.csv', 'a') as new:
                            new.write('%s\t%s\n' % (l[0], l[1]))
                        print 'date -> %s/%s >> %s == file:///home/dundun/桌面/rumour/another/%s' % (category, l[0], l[1], filename)
                    with open('%s%s.csv' % (result_path, category), 'a') as f:
                        f.write('"%s","%s","%s","%s","%s","%s","%s"\n' % (
                            title.encode("utf-8"), l[1], head.encode("utf-8"), date.encode("utf-8"),
                            content.replace('"',"'").encode("utf-8"), category.encode("utf-8"), l[2]))
                else:
                    with open('error.csv', 'a') as error:
                        error.write(line)
    print count
    print parse_count
    print head_count
    print date_count


if __name__ == "__main__":

    clean_all_article()

    '''
    with open('test.html', 'r') as f:
        html = f.read()
    d = get_content10(html)
    print d
    '''

