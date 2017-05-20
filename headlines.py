import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import urllib

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {'publication':'bbc',
            'city': 'London,UK'}

@app.route("/")
#@app.route("/<publication>")

def home():
    #get customized headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    # get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    return render_template("home.html", articles=articles, weather=weather)

def get_news(publication="fox"):
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4c05d9049bb68aed624c9c34778affb3"
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data.decode('utf-8'))
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"], 
        "temperature":parsed["main"]["temp"], 
        "city":parsed["name"]
        }
    return weather


if __name__ == '__main__':
    app.run(port=5000, debug=True)