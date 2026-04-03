from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections


def get_winery_age(today):
    foundation_year = datetime.date(year=1920, month=1, day=1)
    winery_age = today - foundation_year
    return int(winery_age.days // 365.25)


def get_years_name(year):
    if year % 100 in (11, 12, 13, 14):
        return 'лет'
    elif year % 10 == 1:
        return 'год'
    elif year % 10 in (2, 3, 4):
        return 'года'
    else:
        return 'лет'


def get_wines_by_category(wines):
    wines_by_category = collections.defaultdict(list)
    for wine in wines:
        wines_by_category[wine.get('Категория')].append(wine)
    return wines_by_category


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

today = datetime.date.today()

winery_age = get_winery_age(today)

wines = pandas.read_excel(
    'wine3.xlsx',
    na_values='N/A',
    keep_default_na=False
).to_dict(orient='records')

rendered_page = template.render(
    winery_age=winery_age,
    years_name=get_years_name(winery_age),
    wines_by_category=get_wines_by_category(wines),
)


with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)


server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
