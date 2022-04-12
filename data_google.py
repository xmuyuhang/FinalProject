#########################################
##### Name: Yuhang Zheng            #####
##### Uniqname: zyuhang             #####
#########################################

import requests
import json
import webbrowser
import datetime
from tqdm import tqdm

t1 = datetime.datetime.now().timestamp()
GOOGLE_BASEURL = "https://maps.googleapis.com/maps/api/place/nearbysearch"
GOOGLE_API_KEY = 'AIzaSyDziVLztXkhFZi62IzmSp-pmM2T8OjLFkA'
payload={}
headers = {}
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


data_yelp = open_cache('cache_yelp.json')

restaurant_nearby = {}
for each_location in data_yelp.values():
    print(each_location)
    for item in tqdm(each_location,total=len(each_location)):
        lat = item['coordinates']['latitude']
        lng = item['coordinates']['longitude']
        
        item_name = item['name']
        url = GOOGLE_BASEURL+"/json?"+"location="+str(lat)+"%2C"+str(lng)+"&radius=0.5&type=restaurant&keyword=restaurant&key="+GOOGLE_API_KEY
        response = requests.request("GET", url, headers=headers, data=payload) # GOOGLEMAPS API
        nearby_place = json.loads(response.text)['results']
        restaurant_nearby[item_name] = nearby_place
save_cache(restaurant_nearby, 'cache_nearby.json')
t2 = datetime.datetime.now().timestamp()

print("time with caching: ", (t2 - t1) * 1000, "ms")

