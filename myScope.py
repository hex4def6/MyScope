from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/MyScope")

def get_headlines():
    user_pass_dict = {'user': '',
                      'passwd': '',
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'I am testing Alexa: Sentdex'})
    sess.post('https://www.reddit.com/api/login', data = user_pass_dict)
    time.sleep(1)
    url = 'https://reddit.com/r/worldnews/.json?limit=10'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    titles = '... '.join([i for i in titles])
    return titles  

@app.route('/')
def homepage():
    return "MyScope is running!"

@ask.launch
def start_skill():
    welcome_message = 'Starting MyScope!'
    return question(welcome_message)

@ask.intent("NewsIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'The current world news headlines are {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("ExitIntent")
def ExitIntent():
    bye_text = 'Goodbye'
    return statement(bye_text)


@ask.intent("VersionIntent")
def VersionIntent():
    output_text = 'MyScope version is 0.01'
    return statement(output_text)








    
if __name__ == '__main__':
    app.run(debug=True)
