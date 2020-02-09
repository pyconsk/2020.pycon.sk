from datetime import date

from flask import Flask, g, request, render_template, abort, make_response, url_for, redirect
from flask_babel import Babel, gettext, lazy_gettext

from utils import get_news, get_speakers

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
    return render_template('edusummit.html', **_get_template_variables(li_edusummit='active', background='bkg-index',
                                                                       speakers=SPEAKERS))


@app.route('/<lang_code>/thanks.html')
def thanks():
    return render_template('thanks.html', **_get_template_variables(li_cfp='active', background='bkg-index'))


@app.route('/<lang_code>/privacy-policy.html')
def privacy_policy():
    return render_template('privacy-policy.html', **_get_template_variables(li_privacy='active', background='bkg-privacy'))


@app.route('/<lang_code>/speakers/index.html')
def speakers():
    variables = _get_template_variables(li_speakers='active', background='bkg-speaker', speakers=SPEAKERS)

    return render_template('speaker_list.html', **variables)

@app.route('/<lang_code>/speakers/<name>.html')
def profile(name):
    name = ' '.join(name.split('-')).title()
    variables = _get_template_variables(li_speakers='active', background='bkg-speaker')

    for speaker in SPEAKERS:
        if speaker['name'] == name:
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
