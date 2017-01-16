# -*- coding: utf-8 -*-
import requests
from cookielib import CookieJar

url = "http://urbanlegends.about.com/od/government/a/proposed_28th_amendment.htm"
r = requests.get(url)
# print r.text
print r.cookies
