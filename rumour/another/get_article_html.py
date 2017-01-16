# -*- coding: utf-8 -*-
import random
import requests
import glob
import re
import os
import time
import traceback
from cookielib import CookieJar
from pyquery import PyQuery as pq


# get the article's html
def get_html(category, title, url):
    index = True
    count = 0
    while index:
        global r
        try:
            r = requests.get(url, timeout=300)
        except:
            traceback.print_exc()
        if r.status_code == 200:
            index = False
        count += 1
        if count >=10:
            with open('connect_fail.csv', 'a') as error:
                error.write('%s\t\t\t%s\t\t\t%s\n' % (title, url, category))
            break
    html = r.text
    with open('html/%s/%s.html' % (category.replace(' ', '_').replace('&', 'and').replace("'", '').replace('"', ''),
                                   title.replace('/', '-').replace('.', '_')), 'w') as new:
        new.write(html.encode('utf-8'))


def get_all_article_html():
    index = 0
    for filename in glob.glob(r'article_url/*.tsv'):
        print '------ %s start --------' % filename
        category = filename.replace('.tsv', '').replace('article_url/', '')
        cmdline = 'mkdir html/%s' % category.replace(' ', '_').replace('&', 'and').replace("'", '').replace('"', '')
        os.popen(cmdline)
        with open(filename, 'r') as f:
            count = 0
            for line in f:
                l = line.strip().split('\t')
                if len(l) == 2:
                    get_html(category, l[0], l[1])
                else:
                    with open('error.csv', 'a') as error:
                        error.write(line)
                t = random.randint(2, 5)
                time.sleep(t)
                count += 1
            print '>>>>>> count contain %d' % count
        index += count
        print '>>>>>> index contain %d' % index
        print '------ %s end --------' % filename


def get_article_url_from_html(html):
    doc = pq(html)
    div = doc('div[class="widget page-btns-wrapper"]')
    divs1 = div('div[class="col col-1"]')
    dic = dict()
    for div1 in divs1:
        div1 = pq(div1)
        a = div1('a')
        href = a.attr('href')
        num = a.text()
        if href:
            dic[num] = href
    index = 1
    if dic:
        for k in dic.keys():
            if int(k) > index:
                index = int(k)
        if index > 5:
            s = re.search(r'\d.htm$', dic[dic.keys()[0]])
            if s:
                num = s.group().replace('.htm', '')
            for i in range(6, index):
                re_num = int(num) - int(dic.keys()[0]) + i
                href = dic[dic.keys()[0]].replace(num, str(re_num))
                dic[str(i)] = href
    return dic


# get the article's html
def get_html1(category, title, url):
    index = True
    count = 0
    while index:
        global r
        try:
            r = requests.get(url, timeout=300)
        except:
            traceback.print_exc()
        if r.status_code == 200:
            index = False
        count += 1
        if count >=10:
            with open('connect_fail.csv', 'a') as error:
                error.write('%s\t\t\t%s\t\t\t%s\n' % (title, url, category))
            break
    html = r.text
    with open('html1/%s/%s.html' % (category.replace(' ', '_').replace('&', 'and').replace("'", '').replace('"', ''),
                                   title.replace('/', '-').replace('.', '_')), 'w') as new:
        new.write(html.encode('utf-8'))


def get_more_html():
    for directory in glob.glob(r'html/*'):
        for filename in glob.glob(r'%s/*.html' % directory):
            with open(filename, 'r') as f:
                html = f.read()
            dic = get_article_url_from_html(html)
            if dic:
                for num, href in dic.iteritems():
                    print '%s  %s >> %s' % (filename, num, href)
                    get_html1(directory.replace('html/', ''),
                             filename.replace(directory, '').replace('/', '').replace('.html', num), href)


if __name__ == "__main__":
    get_more_html()

