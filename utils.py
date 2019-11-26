import os
import json

from datetime import datetime


def read_json_file(path):
    with open(path) as json_file:
        data = json.load(json_file)

    return data


def get_news(lang='sk'):
    news = []

    for item in read_json_file(os.path.join('data', 'news.json')):
        data = {
            "date": datetime.strptime(item['date'], '%Y-%m-%d').date(),
            "categories": item['categories']
        }

        if lang == "sk":
            data["title"] = item['title_sk']
            data["meta"] = item['meta_sk']

        if lang == "en":
            data["title"] = item['title_en']
            data["meta"] = item['meta_en']

        if 'url' in item.keys():
            data['url'] = item['url']

        news.append(data)

    return news
