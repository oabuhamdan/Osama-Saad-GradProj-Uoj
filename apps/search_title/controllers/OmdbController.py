import requests

key = '3108f83'
api_url = 'http://www.omdbapi.com/?t={1}&y={2}&apikey={0}'


def get_movie_info(name, year):
    url = api_url.format(key, name, year)
    response = requests.get(url)
    json_response = response.json()
    return json_response
