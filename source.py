#!/usr/bin/env python3
import os
from bs4 import BeautifulSoup
from time import sleep
from requests import session
from utils import *

root = 'placement.iitk.ac.in'
url = 'https://placement.iitk.ac.in/login/'

with session() as c:
    html = c.get(url)

    soup = BeautifulSoup(html.content, 'html5lib')
    csrftoken = soup.find("input")['value']
    print(csrftoken)

    payload = {
        'csrfmiddlewaretoken': csrftoken,
        'username': '<username>',
        'password': '<password>'
    }
    post_res = c.post(url, data=payload)
    print(post_res)

    # Get all proformas
    get_proformas(c)

    # Get stats
    get_stats(c)
