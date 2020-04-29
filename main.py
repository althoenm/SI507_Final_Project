import requests
import json
from flask import Flask, render_template, request,redirect, url_for
from datetime import date

app = Flask(__name__)

@app.route('/')
def index():
    today = date.today()
    return render_template('index.html', date=today)

@app.route('/handle_form', methods=['POST'])
def handle_form():
    country = request.form["country"]

    country_url = 'https://corona.lmao.ninja/v2/countries/'
    c_results = requests.get(f"{country_url}{country}").json()
    flag = c_results['countryInfo']['flag']
    c_tot_cases = c_results['cases']
    c_deaths = c_results['deaths']
    c_today_deaths = c_results['todayDeaths']
    c_recovered = c_results['recovered']
    c_active_cases = c_results['active']
    tests = c_results['tests']
    cpm = c_results['casesPerOneMillion']
    dpm = c_results['deathsPerOneMillion']
    tpm = c_results['testsPerOneMillion']

    return render_template('response1.html',
        country=country,
        c_tot_cases=c_tot_cases,
        c_deaths=c_deaths,
        c_today_deaths=c_today_deaths,
        c_recovered=c_recovered,
        c_active_cases=c_active_cases,
        tests=tests,
        cpm=cpm,
        dpm=dpm,
        tpm=tpm,
        flag=flag
        )
    

if __name__ == '__main__':
    app.run(debug=True)
#continent_api_request()
#country_api_request()

