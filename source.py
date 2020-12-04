#!/usr/bin/env python3
import os
from bs4 import BeautifulSoup
from time import sleep
from requests import session

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
    print(post_res.headers)
    sleep(1)
    res = c.get('http://placement.iitk.ac.in/jaf_list/', headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "placement.iitk.ac.in",
        "Pragma": "no-cache",
        "Referer": "https://placement.iitk.ac.in/dashboard/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    })
    print(res)
    print(res.url)
    soup = BeautifulSoup(res.content, 'html5lib')
    profiles = soup.findAll('tr')
    profiles = profiles[1:]
    count = len(profiles)
    print(f"total no. of profiles: {count}")

    custom_header = {
        "Host": "placement.iitk.ac.in",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://placement.iitk.ac.in/jaf_list/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"}

    last_path = None
    cnt = 1
    for i, profile in enumerate(profiles):
        profile = profile.findAll('td')
        job = profile[0].a.text.replace(
            "/", "").replace(".", "").replace(" ", "")
        com_name = profile[1].text.replace(
            "/", "").replace(".", "").replace(" ", "")

        file_path = 'placements20-21/' + com_name + '--' + job + '.html'
        org_path = file_path
        if file_path == last_path:
            file_path = 'placements20-21/' + com_name + \
                '--' + job + str(cnt) + '.html'
            cnt += 1
        else:
            cnt = 1

        last_path = org_path

        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(
                file_path))
        if not os.path.exists(file_path):
            com_link = 'https://placement.iitk.ac.in' + profile[0].a['href']
            res = c.get(com_link, headers=custom_header)
            soup = BeautifulSoup(res.content, 'html5lib')
            data = soup.find('div', attrs={'class': 'text-center'})
            data = '<link href = "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel = "stylesheet" integrity = "sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin = "anonymous" >' + data.prettify()
            print(f"profile no. {i}/{count}")
            file = open(file_path, 'w', encoding='utf-8')
            file.write(data)
            file.close()
            sleep(0.5)
