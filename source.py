#!/usr/bin/env python3
import os
from bs4 import BeautifulSoup
from time import sleep
from requests import session
from utils import *

root = 'placement.iitk.ac.in'
url = 'https://placement.iitk.ac.in/login/'
username = input("Enter Portal Username: ")
password = input("Enter Portal Password: ")
with session() as c:
    html = c.get(url)

    soup = BeautifulSoup(html.content, 'html5lib')
    csrftoken = soup.find("input")['value']
    # print(csrftoken)
    
    payload = {
        'csrfmiddlewaretoken': csrftoken,
        'username': username,
        'password': password
    }
    post_res = c.post(url, data=payload)
    soup = BeautifulSoup(post_res.content, 'html5lib')
    rr = soup.find(id="blog")
    if rr != None:
        print("User does not exist. Please try again with valid credentials :(")
    else:
        print(f"Happy extracting {username} :)")
        # Get all proformas
        get_proformas(c)

        # Get stats
        get_stats(c)