# coding : utf-8
"""
    get_categories.py

    get the categories list html and clean it to get all categories' title and url

"""

import requests
from bs4 import BeautifulSoup


def get_categories_by_html(html):
    soup = BeautifulSoup(html, "html.parser")
    soup.prettify()
    categories = dict()
    flags = soup.find("div", {"class": "td-page-text-content"}).find("pre").find("ul").findAll("li")
    for flag in flags:
        if flag.find("ul"):
            '''
            ul = flag.find("ul").findAll("li")
            print len(ul)
            for li in ul:
                alis = li.find("a")
                print '%s  %s\n' % (alis.text, alis['href'])
                f.write('%s,%s\n' % (alis.text, alis['href']))
                count += 1
            '''
            pass
        else:
            alis = flag.find('a')
            title = alis.text.replace('/', '-').replace('\n', '').replace('\r', '').replace('\t', '')
            href = alis['href'].replace('\n', '').replace('\r', '').replace('\t', '')
            categories[title] = href
    return categories


def get_categories_html(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        # 'Cookie': '__gads=ID=0ef6f4041cc3072e:T=1482027422:S=ALNI_MacqPmuzB3yPg33fWREtPPqjIbWCQ; _omappvp=true; om-450111=true; om-interaction-cookie=true; __atuvc=19%7C51; _gat=1; _ga=GA1.2.268200551.1482027423; advanced_ads_browser_width=946',
        'Host': 'www.truthorfiction.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    r = requests.get(url=url, headers=headers, timeout=300)
    return r.text


if __name__ == "__main__":
    url = "https://www.truthorfiction.com/category/"
    html = get_categories_html(url)
    categories = get_categories_by_html(html)
    for k, v in categories.iteritems():
        print "%s: %s" % (k, v)
