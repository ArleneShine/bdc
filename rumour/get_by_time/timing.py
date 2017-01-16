# coding=utf-8

import time

from categories import get_categories_html, get_categories_by_html
from articles import search_and_input_to_db_by_category


# --------------- 总操作 ------------------
def total_operation():
    url = "https://www.truthorfiction.com/category/"
    html = get_categories_html(url)
    categories = get_categories_by_html(html)
    for categorie, source_url in categories.iteritems():
        search_and_input_to_db_by_category(categorie, source_url)


if __name__ == "__main__":

    while True:
        # ---------设置定时--------
        if time.localtime().tm_min == 0:
            if time.localtime().tm_hour == 0:
                if time.localtime().tm_wday == 0:
                    print "----- %s: Search begin ------" % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    total_operation()
                    print "----- %s: Search end ------" % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                else:
                    time.sleep(3600*24)
            else:
                time.sleep(3600)
        else:
            time.sleep(60)