import dotenv

API_KEY = dotenv.dotenv_values()['API_KEY']
BASE_URL = dotenv.dotenv_values()['BASE_URL']
HEADERS = {
    "Authorization": "Bearer {}".format(API_KEY),
    "Content-Type": "application/json; charset=utf-8"
}
INSTRUMENT = "BTC_USD"
GRANULARITY= "D"
GRANULARITY_SECONDS = 60
PERIOD= "1200"