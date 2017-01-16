# coding : utf-8
"""
    get_article_html.py

    get all the articles' html
"""
import requests
import glob
import Cookie
import os


# get the article's html
def get_html(category, title, url, cook):
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
        r = requests.get(url, headers=headers, cookies=cook, timeout=300)
        if r.status_code == 200:
            index = False
        count += 1
        if count >=10:
            with open('connect_fail.csv', 'a') as error:
                error.write('%s\t\t\t%s\t\t\t%s\n' % (title, url, category))
            break
    html = r.text
    cook = r.cookies
    with open('html/%s/%s_html.csv' % (category.replace(' ', '_'), title.replace('/', '-').replace('.', '_')), 'a') as new:
        new.write(html.encode('utf-8'))
    return cook


if __name__ == "__main__":
    cookie = Cookie.Cookie()
    for filename in glob.glob(r'save_url_time/*.tsv'):
        print '------ %s start --------' % filename
        category = filename.replace('.tsv', '')
        cmdline = 'mkdir ../html/%s' % category.replace(' ', '_')
        os.popen(cmdline)
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                print line
                l = line.strip().split('\t\t\t')
                if len(l) == 3:
                    cookie= get_html(category, l[0], l[1], cookie)
                else:
                    with open('error.csv', 'a') as error:
                        error.write(line)
        print '------ %s end --------' % filename
