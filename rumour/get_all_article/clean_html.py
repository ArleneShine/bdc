# -*- coding: utf-8 -*-
"""
    clean_html.py

    get the summary and truth from all the html and write to the result files
"""

import HTMLParser
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import glob
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

html_parser = HTMLParser.HTMLParser()
result_path = "result/"


# get the summary and truth from the html by pyquery
def clean_html_by_pq(html):
    doc = pq(html)
    divs = doc('div')
    flags = divs.filter('.td-post-text-content')
    extents = divs.filter('.content-source')
    flag_list = list()
    content = flags.text().replace(extents.text(),'')
    for flag in flags.children():
        if pq(flag).is_('p') or pq(flag).is_('font'):
            flag_list.append(flag)
    for flag in flag_list:
        if flag is not None:
            if flag.find('div',{'class': 'td-a-rec td-a-rec-id-content_inline '}) is not None:
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


# get summary and truth from html by bs4
def clean_html(html):
    html = html_parser.unescape(html)
    soup = BeautifulSoup(html, "html.parser")
    soup.prettify()
    flags = soup.find('div', {'class': 'td-post-text-content'}).findAll("p")
    extent = soup.find('div', {'class': 'td-post-text-content'}).find('div', {'class': 'content-source'})
    if extent:
        extent = extent.findAll("p")
        if len(extent) >= 1:
            extent_content = extent[0].text
        else:
            extent_content = "******&&&&&&&&"
    else:
        extent_content = "******&&&&&&&&"
    summry = ""
    truth = ""
    is_truth = False
    for flag in flags:
        text = flag.text.strip().replace('\t',' ')
        if flag.find('div', {'class': 'td-a-rec td-a-rec-id-content_inline '}):
            pass
        else:
            if is_truth:
                if text == extent_content:
                    break
                if re.match(r'^[\s\r\n\t]*$', text):
                    pass
                else:
                    truth += "%s\\n" % text
            else:
                if re.search(r'The[\s\t\r\n]*Truth:', text):
                    is_truth = True
                    if re.search(r'\S+[\s\t\r\n]*The', text):
                        tr = re.search(r'The[\s\t\r\n]*Truth:', text).group()
                        summ = text.split(tr)[0]
                        S = re.search(r'Summary[\s\t\r\n]*of[\s\t\r\n]*eRumor:',text)
                        if S:
                            summry += summ.split(S.group())[-1]
                        else:
                            summry += summ
                    if re.search(r'The[\s\t\r\n]*Truth:\S+', text):
                        tr = re.search(r'The[\s\t\r\n]*Truth:', text).group()
                        truth += text.split(tr)[-1]
                elif re.search(r'Summary[\s\t\r\n]*of[\s\t\r\n]*eRumor:', text):
                    summry = ""
                    summ = re.search(r'Summary[\s\t\r\n]*of[\s\t\r\n]*eRumor:', text).group()
                    summry += text.split(summ)[-1]
                else:
                    summry += "%s\\n" % text

    return summry, truth


# make the time standard
def clean_time(time_str):
    match = re.match(r'[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}T[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}', time_str.strip())
    if match:
        date_time = match.group().replace('T', ' ')
        return date_time
    else:
        return time_str


# delete the article's blank which is not needed
def del_blank(string):
    groups = re.findall(r'\s{2,}', string)
    if groups:
        for group in groups:
            string = string.replace(group, ' ')
    return string.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')


# get all articles' message and write to file
def clean_all(file_path, url_file):
    filename = re.search('/[\s\S]+.tsv', url_file).group().replace('_url', '').replace('.tsv', '.csv')
    with open(result_path+filename, 'w') as new_file:
        new_file.write('"X.Title.","X.Date.","X.Url.","X.Rumor.Summary.","X.The.Truth.","category"\n')
    with open(url_file, 'r') as f:
        lines = f.readlines()
        for l in lines:
            line = l.strip().split('\t\t\t')
            with open('%s/%s_html.csv' % (file_path, line[0].replace('/', '-').replace('.', '_')), 'r') as f1:
                html = f1.read()
                if re.search(r'The[\s\t\r\n]*Truth', html) or re.search(r'Summary[\s\t\r\n]*of[\s\t\r\n]*eRumor', html):
                    summry, truth = clean_html_by_pq(html)
                    if re.match(r'^[\t\r\n]*$', summry) or re.match(r'^[\t\r\n]*$', truth):
                        print l
                    with open(result_path+filename, 'a') as new:
                        date_time = clean_time(line[2])
                        summry = del_blank(summry)
                        truth = del_blank(truth)
                        new.write('"%s","%s","%s","%s","%s","%s"\n' % (
                            line[0].encode("utf-8"), date_time.encode("utf-8"), line[1].encode("utf-8"),
                            summry.encode("utf-8"), truth.encode("utf-8"),
                            filename.replace('/', '').replace('.csv', '').encode("utf-8")))
                else:
                    with open('no_truth.csv', 'a') as new:
                        new.write('"%s","%s","%s"\n' % (line[0], line[1], line[2]))


if __name__ == "__main__":

    url_path = 'save_url_time/'
    html_path = 'html/'
    count = 1
    for url_file in glob.glob(r'%s*.tsv' % url_path):
        file_path = url_file.replace(url_path, html_path).replace('.tsv', '').replace(' ', '_')
        print "------------------- %d -----------------" % count
        print url_file
        print file_path
        clean_all(file_path, url_file)
        count += 1




