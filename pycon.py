import os
from datetime import date

from flask import Flask, g, request, render_template, abort, make_response, url_for, redirect
from flask_babel import Babel, gettext, lazy_gettext

from utils import get_news, get_speakers, get_edu_speakers, get_edu_talks

EVENT = gettext('PyCon SK 2020 | 27 - 29 March 2020 | Bratislava, Slovakia')
DOMAIN = 'https://2020.pycon.sk'
API_DOMAIN = 'https://api.pycon.sk'

LANGS = ('en', 'sk')
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+00:00'

app = Flask(__name__, static_url_path='/static')  # pylint: disable=invalid-name
app.config['BABEL_DEFAULT_LOCALE'] = 'sk'
app.jinja_options = {'extensions': ['jinja2.ext.with_', 'jinja2.ext.i18n']}
babel = Babel(app)  # pylint: disable=invalid-name

CATEGORIES = {
    'conference': lazy_gettext('Conference'),
    'media': lazy_gettext('Media'),
    'speakers': lazy_gettext('Speakers'),
}

SPEAKERS = get_speakers()
EDU_SPEAKERS = get_edu_speakers()
EDU_TALKS = get_edu_talks()
NEWS = get_news()


@app.route('/sitemap.xml')
def sitemap():
    excluded = {'static', 'sitemap'}
    pages = []

    for lang in LANGS:
        for rule in app.url_map.iter_rules():

            if 'GET' in rule.methods and rule.endpoint not in excluded:
                # `url_for` appends unknown arguments as query parameters.
                # We want to avoid that when a page isn't localized.
                values = {'lang_code': lang} if 'lang_code' in rule.arguments else {}

                if 'name' in rule.arguments:
                    for speaker in SPEAKERS:
                        values['name'] = speaker['name'].lower().replace(' ', '-')
                        pages.append(DOMAIN + url_for(rule.endpoint, **values))
                elif 'category' in rule.arguments:
                    for category in CATEGORIES.keys():
                        values['category'] = category
                        pages.append(DOMAIN + url_for(rule.endpoint, **values))
                else:
                    pages.append(DOMAIN + url_for(rule.endpoint, **values))

    sitemap_xml = render_template('sitemap.xml', pages=pages, today=date.today())
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response


@app.route('/')
def root():
    return redirect('sk/index.html')


@app.route('/<lang_code>/index.html')
def index():
    template_vars = _get_template_variables(li_index='active', news=get_news(get_locale(), items=3),
                                            categories=CATEGORIES, background_filename='img/about/header1.jpg',
                                            speakers=SPEAKERS)
    return render_template('index.html', **template_vars)


@app.route('/<lang_code>/news.html')
def news():
    template_vars = _get_template_variables(li_news='active', news=get_news(get_locale()), categories=CATEGORIES,
                                            background='bkg-news')
    return render_template('news.html', **template_vars)


@app.route('/<lang_code>/news/<category>.html')
def news_category(category):
    if category not in CATEGORIES.keys():
        abort(404)

    template_vars = _get_template_variables(li_news='active', categories=CATEGORIES, background='bkg-news')
    news = []

    for item in NEWS:
        if category in item['categories']:
            news.append(item)

    template_vars['news'] = news
    template_vars['category'] = category
    return render_template('news.html', **template_vars)


@app.route('/<lang_code>/coc.html')
def coc():
    return render_template('coc.html', **_get_template_variables(li_coc='active', background='bkg-chillout'))


@app.route('/<lang_code>/faq.html')
def faq():
    return render_template('faq.html', **_get_template_variables(li_faq='active', background='bkg-chillout'))


@app.route('/<lang_code>/venue.html')
def venue():
    return render_template('venue.html', **_get_template_variables(li_venue='active', background='bkg-chillout'))


@app.route('/<lang_code>/aboutus.html')
def aboutus():
    return render_template('aboutus.html', **_get_template_variables(li_aboutus='active', background='bkg-index'))


@app.route('/<lang_code>/tickets.html')
def tickets():
    return render_template('tickets.html', **_get_template_variables(li_tickets='active', background='bkg-index'))


@app.route('/<lang_code>/cfp.html')
def cfp():
    return render_template('cfp.html', **_get_template_variables(li_cfp='active', background='bkg-speaker'))


@app.route('/<lang_code>/cfp_form.html')
def cfp_form():
    return render_template('cfp_form.html', **_get_template_variables(li_cfp='active', background='bkg-workshop'))


@app.route('/<lang_code>/recording.html')
def recording():
    return render_template('recording.html', **_get_template_variables(li_recording='active', background='bkg-snake'))


@app.route('/<lang_code>/cfv.html')
def cfv():
    return render_template('cfv.html', **_get_template_variables(li_cfv='active', background='bkg-cfv'))


@app.route('/<lang_code>/sponsors.html')
def sponsors():
    return render_template('sponsors.html', **_get_template_variables(li_sponsors='active', background='bkg-index'))


@app.route('/<lang_code>/edusummit.html')
def edusummit():

    FRIDAY = [
        {
            'time': '9:25 - 9:30',
            'speakers': ['Eva Klimeková'],
            'talk': 'Otvorenie 4. ročníka EduSummit na PyCon SK',
        },
        {
            'time': '9:30 - 9:45',
            'talk': 'Učíme s hardvérom'
        },
        {
            'time': '9:45 - 10:15',
            'talk': 'Finále súťaže SPy Cup'
        },
        {
            'time': '10:20 - 10:50',
            'talk': 'Vzbuďme v študentoch chuť programovať!'
        },
        {
            'time': '11:05 - 12:05',
            'talk': 'Ako sa dá s Python zvládnuť štvorročné štúdium na strednej škole',
            'keynote': 'True'
        },
        {
            'time': '13:10 - 13:35',
            'talk': 'EDUTalks'
        },
        {
            'time': '13:35- 13:55',
            'speakers': ['Peter Palát'],
            'talk': 'Internetová bezpečnosť: základy sebaobrany'
        },
        {
            'time': '14:00- 14:30',
            'talk': "Programujeme v Pythone hardvér",
        },
        {
            'time': '14:45- 15:30',
            'talk': "Python ako nástroj pre STE(A)M problémy a úlohy",
        },
        {
            'time': '15:35- 16:05',
            'talk': "Programovací jazyk Robot Karel po novom a online.",
        },
        {
            'time': '16:20- 16:50',
            'talk': 'Vyhlásenie výsledkov SPy Cup a Python Cup'
        },
        {
            'time': '16:55- 17:25',
            'talk': "Z maturity v pascale na pythonovskú novú maturitu, študenstká mobilná apka o pythone v pythone a jednoduché grafické rozhranie pomocou libreoffice calc",
        }
    ]

    FRIDAY2 = [
        {
            'time': '11:05- 12:10',
            'talk': "Programovanie vlastných micro:bit herných ovládačov a autíčok",
        },
        {
            'time': '13:10 - 13:55',
            'talk': "Životopis predáva",
        },
        {
            'time': '14:00 - 16:00',
            'talk': "Buď SMART s micro:bitom",
        }
    ]

    SATURDAY = [
        {
            'time': '9:00 - 10:50',
            'talk': "Robíme IoT na mikrokontroléri ESP32 v jazyku MicroPython"
        },
        {
            'time': '11:05 - 12:10',
            'talk': "Jednoduchý blog vo Flasku",
        },
        {
            'time': '13:10 - 15:00',
            'talk': "Buď SMART s micro:bitom",
        },
        {
            'time': '15:20 - 16:50',
            'speakers': ['Jaroslav Výbošťok', 'Marek Mansell'],
            'talk': "Využitie otvorených dát a GPS s použitím tkinter a Jupyter"
        }
    ]

    SATURDAY2 = [
        {
            'time': '9:00 - 10:50',
            'talk': "Zábava a informatika idú ruka v ruke ! :)",
        },
        {
            'time': '11:05 - 12:10',
            'talk': "Naučte sa programovať s CoderDojo",
        },
        {
            'time': '13:10 - 14:10',
            'talk': "Naprogramuj si robota Ozobot EVO",
        },
    ]

    for spot in FRIDAY:
        for talk in EDU_TALKS:
            if spot['talk'] == talk['title']:
                spot['talk'] = talk
                spot['speakers'] = talk['speakers']
                continue

    for spot in FRIDAY2:
        for talk in EDU_TALKS:
            if spot['talk'] == talk['title']:
                spot['talk'] = talk
                spot['speakers'] = talk['speakers']
                continue

    for spot in SATURDAY:
        for talk in EDU_TALKS:
            if spot['talk'] == talk['title']:
                spot['talk'] = talk
                spot['speakers'] = talk['speakers']
                continue

    for spot in SATURDAY2:
        for talk in EDU_TALKS:
            if spot['talk'] == talk['title']:
                spot['talk'] = talk
                spot['speakers'] = talk['speakers']
                continue

    return render_template('edusummit.html', **_get_template_variables(li_edusummit='active', background='bkg-index',
                                                                       friday=FRIDAY, saturday=SATURDAY,
                                                                       friday2=FRIDAY2, saturday2=SATURDAY2,
                                                                       speakers=EDU_SPEAKERS, talks=EDU_TALKS))


@app.route('/<lang_code>/thanks.html')
def thanks():
    return render_template('thanks.html', **_get_template_variables(li_cfp='active', background='bkg-index'))


@app.route('/<lang_code>/privacy-policy.html')
def privacy_policy():
    return render_template('privacy-policy.html', **_get_template_variables(li_privacy='active', background='bkg-privacy'))


@app.route('/<lang_code>/program/index.html')
def program():
    variables = _get_template_variables(li_program='active', background='bkg-speaker', speakers=SPEAKERS)

    return render_template('program.html', **variables)

@app.route('/<lang_code>/speakers/index.html')
def speakers():
    variables = _get_template_variables(li_speakers='active', background='bkg-speaker', speakers=SPEAKERS+EDU_SPEAKERS)

    return render_template('speaker_list.html', **variables)

@app.route('/<lang_code>/speakers/<name>.html')
def profile(name):
    name = ' '.join(name.split('-')).title()
    variables = _get_template_variables(li_speakers='active', background='bkg-speaker')

    for speaker in SPEAKERS+EDU_SPEAKERS:
        if speaker['name'].lower() == name.lower():
            variables['speaker'] = speaker
            break

    return render_template('speaker.html', **variables)


@app.route('/<lang_code>/countdown.html')
def countdown():
    template_vars = _get_template_variables(li_index='active', background='bkg-index')
    return render_template('countdown.html', **template_vars)


def _get_template_variables(**kwargs):
    """Collect variables for template that repeats, e.g. are in body.html template"""
    variables = {
        'title': EVENT,
        'domain': DOMAIN,
        'lang_code': get_locale(),
    }
    variables.update(kwargs)

    return variables


@app.before_request
def before():  # pylint: disable=inconsistent-return-statements
    if request.view_args and 'lang_code' in request.view_args:
        g.current_lang = request.view_args['lang_code']
        if request.view_args['lang_code'] not in LANGS:
            return abort(404)
        request.view_args.pop('lang_code')


@babel.localeselector
def get_locale():
    # try to guess the language from the user accept
    # header the browser transmits. The best match wins.
    # return request.accept_languages.best_match(['de', 'sk', 'en'])
    return g.get('current_lang', app.config['BABEL_DEFAULT_LOCALE'])
