import requests
import json
import pycountry

BASEURL = 'https://corona.lmao.ninja/'
CACHE_FILENAME = 'cache.json'
CACHE_DICT = {}

# us = requests.get('https://corona.lmao.ninja/v2/jhucsse').json()
# print(us)

# def load_cache_file():
#     try:
#         with open(CACHE_FILENAME, 'r') as cache_file:
#             contents = cache_file.read()
#             cache = json.loads(contents)
#     except:
#         cache = {}
#     return cache

# def save_cache_file(cache):

#     with open (CACHE_FILENAME, 'w') as cache_file:
#         written_contents = json.dumps(cache)
#         cache_file.write(written_contents)

# def url_request_using_cache(url,cache):
#     if url in cache.keys():
#         print('Using cache...')
#         return cache[url]
#     else:
#         print('Fetching...')
#         response = requests.get(url)
#         cache[url] = response.text
#         save_cache_file(cache)
#         return cache[url]

def continent_api_request():
    url = 'https://corona.lmao.ninja/v2/continents/'
    continents = ['north america', 'europe', 'asia', 'south america', 'oceania', 'africa']
    connector = '%20'
    query = input(f'Enter one of the following continents for up to date COVID-19 figures: North America, Europe, Asia, South America, Oceania, Africa: ')

    if query.lower() not in continents:
        print("That is not a valid selection, please try again")
    else:
        params = connector.join(query)
        response = requests.get(url, params=params)
        return print(response.json())

def country_api_request():
    url = 'https://corona.lmao.ninja/v2/countries/'
    connector = '%20'
    query = input(f'Enter the name of a country or ISO2/ISO3 code for up to date COVID-19 figures: ')
    params = connector.join(query)
    response = requests.get(url, params=params)
    if response.status_code==404:
        return print(f'That was not a valid entry. Please try again.')
    else:
        return print(requests.get(f'{url}{query.lower()}').json())

#continent_api_request()
country_api_request()