from datetime import date
from os import listdir
from os.path import isfile, join

from flask import Flask, g, request, render_template, abort, make_response, url_for, redirect
from flask_babel import Babel, gettext

EVENT = gettext('PyCon SK 2020 | 27 - 29 March 2020 | Bratislava, Slovakia')
DOMAIN = 'https://2020.pycon.sk'
API_DOMAIN = 'https://api.pycon.sk'

LANGS = ('en', 'sk')
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+00:00'

app = Flask(__name__, static_url_path='/static')  # pylint: disable=invalid-name
app.config['BABEL_DEFAULT_LOCALE'] = 'sk'
app.jinja_options = {'extensions': ['jinja2.ext.with_', 'jinja2.ext.i18n']}
babel = Babel(app)  # pylint: disable=invalid-name

TAGS = {
    'conference': gettext('Conference'),
    'media': gettext('Media'),
    'speakers': gettext('Speakers'),
}

NEWS = (
    {
        'date': date(2019, 11, 23),
        'title': gettext('Conference chat.'),
        'meta': gettext('Last year we have used Slack as our conference chat so you can get in touch with organizers '
                        'and also with fellow participants. For PyCon SK 2020 chat we are going to use the Slack.'),
        'tags': ('media',),
        'url': 'https://join.slack.com/t/pyconsk/shared_invite/enQtODQ4NjU1NzM2NzI3LTA2ZGNiOTA4YzM5OWM3NmQyZjAxMDlmNzJj'
               'OGIzNjM4ZjEwZGI0MTJiYzAxZmNhZmVjMTZjZjliNWQ4ZjVlNjE',
    },
    {
        'date': date(2019, 11, 16),
        'title': gettext('First batch of speakers.'),
        'meta': gettext('We are honoured to announce the first batch of speakers that will be part of PyCon SK 2020.'),
        'tags': ('speakers',),
    },
    {
        'date': date(2019, 11, 15),
        'title': gettext('We celebrate the Day of Fighting for Freedom and Democracy.'),
        'meta': gettext('On 17th November we celebrate the Day of Fighting for Freedom and Democracy. Thanks to this '
                        'event we can freely organize PyCon SK. We want you to celebrate with us. During the holiday '
                        'you can use 17&#37; discount for tickets using discount code "30-rokov-slobody".'),
        'tags': ('conference',),
        'url': 'https://en.wikipedia.org/wiki/Velvet_Revolution',
    },
    {
        'date': date(2019, 10, 20),
        'title': gettext('The Call for Proposals is open!'),
        'meta': gettext('Do you know anyone in underrepresented group in IT who would like to do a conference talk?'
                        ' Let us know, and try to encourage him/her to submit Call for Proposals for PyCon SK 2020.'
                        'We are trying to support diversity. Anyone can be part of the conference.'),
        'tags': ('speakers',),
    },
)


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
    return render_template('index.html', **_get_template_variables(li_index='active', news=NEWS, tags=TAGS))


@app.route('/<lang_code>/news.html')
def news():
    return render_template('news.html', **_get_template_variables(li_news='active', news=NEWS, tags=TAGS))


@app.route('/<lang_code>/coc.html')
def coc():
    return render_template('coc.html', **_get_template_variables(li_coc='active'))


@app.route('/<lang_code>/tickets.html')
def tickets():
    return render_template('tickets.html', **_get_template_variables(li_tickets='active'))


@app.route('/<lang_code>/cfp.html')
def cfp():
    return render_template('cfp.html', **_get_template_variables(li_cfp='active'))


@app.route('/<lang_code>/cfp_form.html')
def cfp_form():
    return render_template('cfp_form.html', **_get_template_variables(li_cfp='active'))


@app.route('/<lang_code>/recording.html')
def recording():
    return render_template('recording.html', **_get_template_variables(li_recording='active'))


@app.route('/<lang_code>/cfv.html')
def cfv():
    return render_template('cfv.html', **_get_template_variables(li_cfv='active'))


@app.route('/<lang_code>/thanks.html')
def thanks():
    return render_template('thanks.html', **_get_template_variables(li_cfp='active'))


@app.route('/<lang_code>/privacy-policy.html')
def privacy_policy():
    return render_template('privacy-policy.html', **_get_template_variables(li_privacy='active'))


@app.route('/<lang_code>/countdown.html')
def countdown():
    return render_template('countdown.html', **_get_template_variables(li_index='active'))


def _get_template_variables(**kwargs):
    """Collect variables for template that repeats, e.g. are in body.html template"""
    variables = {
        'title': EVENT,
        'domain': DOMAIN,
    }
    variables.update(kwargs)

    if 'current_lang' in g:
        variables['lang_code'] = g.current_lang
    else:
        variables['lang_code'] = app.config['BABEL_DEFAULT_LOCALE']

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
