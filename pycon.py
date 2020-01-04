from datetime import date

from flask import Flask, g, request, render_template, abort, make_response, url_for, redirect
from flask_babel import Babel, gettext, lazy_gettext

from utils import get_news

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

SPEAKERS = (
    {
        'name': 'Tom Dyson',
        'bio': 'Tom graduated from Balliol College, Oxford, in 1995, swapping the later philosophy of Wittgenstein for '
               'Netscape 2 and a 9600 baud modem. He ran a little agency called Naïve (“Why don’t you just call '
               'yourselves ‘Stupid’?”) until he joined forces with Olly in 2000, starting Torchbox with the aim of '
               'building beautiful online software for people who make the world a better place. As Technical Director,'
               ' Tom is responsible for making sure the things we build are fast and reliable and easy to maintain. He '
               'manages the tech team and account directs many of our large technical projects. Along with Olly, Tom '
               'tries to make Torchbox a fun and inspiring place to work. Tom lives with his family in the countryside.'
               ' He reads novels and gets cross at tennis. He plays in three bands who will probably never make it. He '
               'composed the theme tune to Charlie and Lola.',
        'country': 'UK',
        'avatar': 'img/speakers/tom_dyson.jpg',
        'links': {
            'linkedin': 'https://www.linkedin.com/in/tomdyson/',
            'link': 'https://torchbox.com/team/tom-dyson/',
        }
    },
    {
        'name': 'Hannah Hazi',
        'bio': 'I am an Engineer based in Cambridge, UK. I currently work at Stratasys as a C++, Python and Typescript '
               'developer, working on tools to support our GrabCAD Print software. In my spare time I love tinkering '
               'with Raspberry Pi and playing complicated board games.',
        'country': 'UK',
        'avatar': 'img/speakers/female.png',
        'links': {
        }
    },
    {
        'name': 'Nicholas Thapen',
        'bio': 'Nick is a founder of Sourcery, a startup that is using AI to help everyone write better code faster. '
               'He is a developer and architect with over a decade of experience in both academia and industry. '
               'He worked on machine learning and Twitter analytics at Imperial College London, and has also spent '
               'time as a developer and architect in the financial sector.',
        'avatar': 'img/speakers/nick_thapen.png',
        'links': {
            'linkedin': 'https://www.linkedin.com/in/nicholas-thapen/',
            'twitter': 'https://twitter.com/nthapen',
            'link': 'https://sourcery.ai/',
        }
    },
    {
        'name': 'Roman Imankulov',
        'bio': 'Roman is a software developer who started his career creating web apps with Django before it was cool. '
               'Eventually he sticks to Python for more than a decade, successfully using it as a golden hammer it to '
               'solve all kinds of problems. Originally Russian, at the moment he lives in Porto and works at Doist as '
               'head of the back-end development team.',
        'avatar': 'img/speakers/roman_imankulov.jpg',
        'links': {
            'linkedin': 'https://www.linkedin.com/in/roman-imankulov-91076144/',
            'twitter': 'https://twitter.com/rdotpy',
            'github': 'https://github.com/imankulov',
        }
    },
)

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

                if 'category' in rule.arguments:
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
    template_vars = _get_template_variables(li_index='active', news=get_news(get_locale()), categories=CATEGORIES,
                                            background_filename='img/about/header1.jpg', speakers=SPEAKERS)
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
    return render_template('news.html', **template_vars)


@app.route('/<lang_code>/coc.html')
def coc():
    return render_template('coc.html', **_get_template_variables(li_coc='active', background='bkg-chillout'))


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


@app.route('/<lang_code>/thanks.html')
def thanks():
    return render_template('thanks.html', **_get_template_variables(li_cfp='active', background='bkg-index'))


@app.route('/<lang_code>/privacy-policy.html')
def privacy_policy():
    return render_template('privacy-policy.html', **_get_template_variables(li_privacy='active', background='bkg-privacy'))


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
