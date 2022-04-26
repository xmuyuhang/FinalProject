import requests
import json
import webbrowser
import datetime
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

data_yelp = open_cache('cache_yelp.json')
data_nearby = open_cache('cache_nearby.json')
for location in data_yelp.values():
    for item in location:
        print(item)
        break
    break

