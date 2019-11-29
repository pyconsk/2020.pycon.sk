from datetime import datetime, date
import os
import json
from flask import url_for
from flask_babel import gettext as _

from settings import LANGUAGES, DOMAIN


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


def get_speakers():
    return read_json_file(os.path.join('data', 'speakers.json'))


def rss_date(pub_date=None):
    """
    Reformats date string from YYYY-MM-DD to RSS pubDate following RFC822
    in CET timezone (hardcoded)
    """
    if pub_date is None:
        pub_date = date(2019, 10, 1)
    rss_formatted = pub_date.strftime("%a, %d %b %Y %H:%M:%S +0100")
    return rss_formatted


def get_guid(title, pub_date):
    # RSS validator requires GUID if multiple items
    # as we do not use database, hash of date + title to get unique result is used
    title = title[:20] + max(20 - len(title), 0) * '='
    unique = ':'.join([pub_date.strftime('%Y-%m-%d'), title])
    return str(hash(unique)).replace('-', 'X')


def fix_url(url):
    if url.startswith('/') and not url.startswith('http://') and not url.startswith('https://'):
        url = DOMAIN + url
    return url


def get_item(story):
    title = story.get('title', _('Unnamed message'))
    pub_date = story.get('date')
    return {
        'title': title,
        'link': fix_url(story.get('url', DOMAIN)),
        'description': story.get('meta', ''),
        'pubdate': rss_date(pub_date),
        'categories': story.get('categories', []),
        'guid': get_guid(title, pub_date)
    }


def get_rss(lang=None):
    """
    Generate RSS according to https://www.w3schools.com/XML/xml_rss.asp
    As an input it uses data from /data/news.json
    :param lang: string, if None fallback to default 'sk'
    :return: RSS xml
    """
    if not lang or lang not in LANGUAGES:
        lang = 'sk'
    news = get_news(lang)
    ordered_news = sorted(news, key=lambda x: x.get('date'), reverse=True)
    items = [get_item(story) for story in ordered_news]

    return {
        'title': _('PyCon SK 2020 Newsroom'),
        'link': url_for('news', lang_code=lang),
        'description': _('News from PyCon Sk 2020 community conference'),
        'language': lang,
        'items': items
    }
