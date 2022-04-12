#########################################
##### Name: Yuhang Zheng            #####
##### Uniqname: zyuhang             #####
#########################################

import requests
import json
import webbrowser
import datetime
from secret import YELP_API_KEY


def open_cache(CACHE_FILENAME):
    ''' opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict, CACHE_FILENAME):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()

# top 30 cities in the U.S. by population
list_of_state = ['New York', 'Los Angeles', 'Chicago', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'Houston', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Indianapolis', 'Charlotte', 'San Francisco', 'Seattle', 'Denver', 'Washington, DC', 'Nashville-Davidson', 'Oklahoma City', 'El Paso', 'Boston', 'Portland', 'Las Vegas', 'Detroit', 'Memphis', 'Louisville-Jefferson County', 'Baltimore']
YELP_BASEURL = "https://api.yelp.com/v3/businesses/search"


payload={}
headers = {}

HEADERS = {'Authorization':  'bearer %s' %YELP_API_KEY}
five_state = {}
for location in list_of_state:
    PARAMETERS = {'location': location, 'categories': 'restaurants', 'sort_by':'best_match', 'limit': '50'}
    response = requests.get(url = YELP_BASEURL,params = PARAMETERS,headers = HEADERS) # YELP API
    restaurant = json.loads(response.text)
    
    five_state[location] = restaurant['businesses']
save_cache(five_state, 'cache_yelp.json')