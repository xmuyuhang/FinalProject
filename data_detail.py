#########################################
##### Name: Yuhang Zheng            #####
##### Uniqname: zyuhang             #####
#########################################

import requests
import json
import webbrowser
import datetime
from tqdm import tqdm
from secret import GOOGLE_API_KEY

t1 = datetime.datetime.now().timestamp()
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

GOOGLE_BASEURL = "https://maps.googleapis.com/maps/api/place/details/json?"


nearby_detail = {}
data_nearby = open_cache('cache_nearby.json')
for item in data_nearby.values():
    for res in tqdm(item, total=len(item)):
        print(res['name'])
        item_name = res['name']
        url = GOOGLE_BASEURL+"place_id="+str(res['place_id'])+"&fields=name%2Crating%2Cformatted_phone_number%2Crating%2Cformatted_address%2Crating%2Cwebsite&key="+GOOGLE_API_KEY
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        detail = json.loads(response.text)
        if detail['status']=='OK':
            nearby_detail[item_name] = detail['result']
        else:
            nearby_detail[item_name] = None
        

save_cache(nearby_detail, 'nb_detail.json')
t2 = datetime.datetime.now().timestamp()

print("time with caching: ", (t2 - t1) * 1000, "ms")