# coding: utf-8

import requests
import Cookie
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def get_url_by_categories(category, source_url, cook):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    index = True
    while index:
        global r
        r = requests.get(source_url, headers=headers, cookies=cook, timeout=300)
        if r.status_code == 200:
            index = False
    cook = r.cookies
    html = r.text
    num = get_page_num(html)
    if num == -1:
        print '%s : %s - num wrong' % (category, source_url)
    get_url_by_html(html, category)
    for i in range(2, num+1):
        second_url = source_url+"page/%d" % i
        index = True
        while index:
            global r1
            r1 = requests.get(second_url, headers=headers, cookies=cook, timeout=300)
            if r1.status_code == 200:
                index = False
            else:
                index = True
        cook = r1.cookies
        html = r1.text
        get_url_by_html(html, category)
    return cook


def get_url_by_html(html, category):
    soup = BeautifulSoup(html, "html.parser")
    soup.prettify()
    flags = soup.findAll("div", {"class": "item-details"})
    with open('url_time/%s_url.tsv' % category, 'a') as new:
        for flag in flags:
            alis = flag.find("a")
            t = flag.find("time")
            a_time = t['datetime'].replace('\n', '').replace('\r', '').replace('\t', '')
            title = alis['title'].replace('\n', '').replace('\r', '').replace('\t', '')
            href = alis['href'].replace('\n', '').replace('\r', '').replace('\t', '')
            print '%s\t%s\n' % (title, href)
            new.write('%s\t\t\t%s\t\t\t%s\n' % (title, href, a_time))


def get_page_num(html):
    words = re.search(r'Page\s\d+\sof\s\d+', html)
    if words:
        words = words.group()
        part = re.match('Page\s\d+\sof\s', words)
        num = words.replace(part.group(), '')
        return int(num)
    else:
        return -1


if __name__ == "__main__":
    cookie = Cookie.Cookie()
    with open('categories_url.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            print '------------------------------'
            print line
            print '------------------------------'
            line = line.strip().split('\t')
            cookie = get_url_by_categories(line[0], line[1], cookie)
            print cookie

