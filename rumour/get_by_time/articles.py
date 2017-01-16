# coding=utf-8
"""
    articles.py

    some operation about article'url and html
"""

import re
import requests
import traceback
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from mysql_operation import get_title_category_from_db, insert_one_data


# search if the article is existed in database and put it to db or ignore
def search_and_input_to_db_by_category(category, source_url):
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
    c = 0
    while index:
        global r
        r = requests.get(source_url, headers=headers, timeout=300)
        if r.status_code == 200:
            index = False
        c += 1
        if c > 10:
            break
    html = r.text
    num = 1
    is_flag = True
    while is_flag:
        data = get_url_by_html(html)
        title_category = get_title_category_from_db()
        for dic in data:
            if [dic['title'], category] in title_category:
                is_flag = False
                break
            else:
                article_html = get_html(category, dic['title'], dic['href'])
                if re.search(r'The[\s\t\r\n]*Truth', article_html) or re.search(r'Summary[\s\t\r\n]*of[\s\t\r\n]*eRumor', article_html):
                    summary, truth = get_message_by_html(article_html)
                    try:
                        insert_one_data(dic['title'], dic['date'], dic['href'], summary, truth, category)
                        print "insert_data: %s, %s, %s, %s\n" % (dic['title'], dic['date'], dic['href'], category)
                    except:
                        traceback.print_exc()
                        with open("input_to_db_fail.csv", 'a') as f:
                            f.write('"%s","%s","%s","%s","%s","%s"\n' %
                                    (dic['title'], dic['date'], dic['href'], summary, truth, category))
                else:
                    with open('no_truth.csv', 'a') as new:
                        new.write('"%s","%s","%s","%s"\n' % (dic['title'], dic['date'], dic['href'], category))
        num += 1
        if is_flag:
            second_url = source_url+"page/%d" % num
            index = True
            while index:
                global r1
                r1 = requests.get(second_url, headers=headers, timeout=300)
                if r1.status_code == 200:
                    index = False
                else:
                    index = True
            html = r1.text
            get_url_by_html(html)
    return True


# get the article's html
def get_html(category, title, url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'www.truthorfiction.com',
        'Referer': 'https://www.truthorfiction.com/category/natural-disasters/hurricane/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    index = True
    count = 0
    while index:
        global r
        r = requests.get(url, headers=headers, timeout=300)
        if r.status_code == 200:
            index = False
        count += 1
        if count >=10:
            with open('connect_fail.csv', 'a') as error:
                error.write('%s\t\t\t%s\t\t\t%s\n' % (title, url, category))
            break
    html = r.text
    return html


# get the article's title, url, date from the html
def get_url_by_html(html):
    soup = BeautifulSoup(html, "html.parser")
    soup.prettify()
    flags = soup.findAll("div", {"class": "item-details"})
    data = list()
    for flag in flags:
        alis = flag.find("a")
        t = flag.find("time")
        a_time = t['datetime'].replace('\n', '').replace('\r', '').replace('\t', '')
        title = alis['title'].replace('\n', '').replace('\r', '').replace('\t', '')
        href = alis['href'].replace('\n', '').replace('\r', '').replace('\t', '')
        data.append({'title': title, 'href': href, 'date': a_time})
    return data


# get the truth and summary from article's html
def get_message_by_html(html):
    doc = pq(html)
    divs = doc('div')
    flags = divs.filter('.td-post-text-content')
    extents = divs.filter('.content-source')
    flag_list = list()
    content = flags.text().replace(extents.text(), '')
    for flag in flags.children():
        if pq(flag).is_('p') or pq(flag).is_('font'):
            flag_list.append(flag)
    for flag in flag_list:
        if flag is not None:
            if flag.find('div', {'class': 'td-a-rec td-a-rec-id-content_inline '}) is not None:
                content.replace(flag.text, '')
    content = content.replace('surgeprice.display("truthorfiction.com_728x90_adsense-midpage-728x90");', '')
    if re.search(r'Summary[\s\t\r\n]*of[\s\t\r\n]*eRumor:', content):
        summ = re.search(r'Summary[\s\t\r\n]*of[\s\t\r\n]*eRumor:', content).group()
        content = content.split(summ)
        if len(content) == 3:
            return content[1], content[2]
        content = content[-1]
    elif re.search(r'Summary[\s\t\r\n]*of[\s\t\r\n]*eRumor', content):
        summ = re.search(r'Summary[\s\t\r\n]*of[\s\t\r\n]*eRumor', content).group()
        content = content.split(summ)
        if len(content) == 3:
            return content[1], content[2]
        content = content[-1]
    summary = ""
    if re.search(r'The[\s\t\r\n]*Truth:', content):
        tr = re.search(r'The[\s\t\r\n]*Truth:', content).group()
        summary = content.split(tr)[0]
        truth = content.split(tr)[-1]
    elif re.search(r'The[\s\t\r\n]*Truth', content):
        tr = re.search(r'The[\s\t\r\n]*Truth', content).group()
        summary = content.split(tr)[0]
        truth = content.split(tr)[-1]
    elif re.search(r'he[\s\t\r\n]*Truth:', content):
        tr = re.search(r'he[\s\t\r\n]*Truth', content).group()
        summary = content.split(tr)[0]
        truth = content.split(tr)[-1]
    elif re.search(r'Truth:', content):
        tr = re.search(r'Truth:', content).group()
        summary = content.split(tr)[0]
        truth = content.split(tr)[-1]
    else:
        truth = content
    return summary, truth




