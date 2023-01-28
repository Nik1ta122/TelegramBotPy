import requests
from bs4 import BeautifulSoup

from datetime import date, datetime, timedelta

import re


def get_school_news():
    url = 'https://sch1448.mskobr.ru/novosti'
    response = requests.get(url).text

    soup = BeautifulSoup(response, 'html.parser')

    news_list = soup.find_all('div', class_='kris-news-box')

    last_news_list = []  # список новостей, каждая новость - словарь

    today = date.today()

    for post in news_list:
        post_birthday = post.find('div', class_='kris-news-data-txt').text.strip()
        post_birthday = datetime.strptime(post_birthday, "%d.%m.%Y").date()

        if post_birthday > today - timedelta(days=7):
            title = post.find('div', class_='h3').text.strip()

            text = post.find('p').text.strip()[:100]
            if text != '':
                text = text + '..'

            img = post.find('img')

            if img is not None:
                pattern = 'src=".+"'
                img_url = re.search(pattern, str(img)).string[10:][:-3]
                img_url = 'https://sch1448.mskobr.ru' + img_url
            else:
                img_url = 'https://na-zapade-mos.ru/files/data/user/AiF/' + \
                          'olga.k/files/2020/2021.06.21-1624286593.4332_2021.06.21-1624279282.1772-dscf4762.jpg'

            post_url = post.find('a', class_='link_more').get('href')
            post_url = 'https://sch1448.mskobr.ru' + post_url

            one_post_info = {
                'data': post_birthday,
                'title': title,
                'text': text,
                'img_url': img_url,
                'post_url': post_url
            }
            last_news_list.append(one_post_info)

    return last_news_list



