# coding : utf-8
"""
    get_categories.py

    get all categories' title and url and save to file

"""

from bs4 import BeautifulSoup


def get_categories(html):
    count = 0
    soup = BeautifulSoup(html, "html.parser")
    soup.prettify()
    flags = soup.find("div", {"class": "td-page-text-content"}).find("pre").find("ul").findAll("li")
    with open('categories_url.csv', 'w') as f:
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
                print '%s  %s\n' % (title, href)
                f.write('%s\t%s\n' % (title, href))
                count += 1
    return count


if __name__ == "__main__":
    with open('categories.csv', 'r') as f:
        html = f.read()
    print get_categories(html)
