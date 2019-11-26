import os
import json

from datetime import datetime
from flask_babel import gettext


def read_json_file(path):
    with open(path) as json_file:
        data = json.load(json_file)

    return data


def get_news():
    news = []

    for item in read_json_file(os.path.join('data', 'news.json')):
        data = {
            "date": datetime.strptime(item['date'], '%Y-%m-%d').date(),
            "title": gettext(item['title']),
            "meta": gettext(item['meta']),
            "categories": item['categories']
        }

        if 'url' in item.keys():
            data['url'] = item['url']

        news.append(data)

    return news
