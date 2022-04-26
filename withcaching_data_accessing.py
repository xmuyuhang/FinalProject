#########################################
##### Name: Yuhang Zheng            #####
##### Uniqname: zyuhang             #####
#########################################

import requests
import json
import webbrowser
import datetime

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

data_yelp = open_cache('cache_yelp.json')
data_nearby = open_cache('cache_nearby.json')
data_detail = open_cache('nb_detail.json')
thirty_state = {}
for location,each_info in data_yelp.items():
    each_item = []
    for item in each_info:
        item_dict = {}
        if 'delivery' in item['transactions']:
            item_dict['delivery or not'] = 'Yes'
        else:
            item_dict['delivery or not'] = 'No'
        item_dict['name'] = item['name']
        item_dict['address'] =item['location']['display_address']
        item_dict['phone'] = item['display_phone']
        item_dict['rating'] =item['rating']
        item_dict['link'] = item['url']
        item_dict['image'] = item['image_url']
        item_dict['type'] = item['categories'][0]['title']
        if 'price' in item.keys():
            if item['price'] == '$':
                item_dict['price'] = '1'
            elif item['price'] == '$$':
                item_dict['price'] = '2'
            elif item['price'] == '$$$':
                item_dict['price'] = '3'
            elif item['price'] == '$$$$':
                item_dict['price'] = '4'
            elif item['price'] == '$$$$$':
                item_dict['price'] = '5'
        else:
            item_dict['price'] = 'no price'
        
        all_nearby = []
        nearby_place = data_nearby[item_dict['name']]
        for place in nearby_place:
            each_nearby = {}
            each_nearby['name'] = place['name']
            each_nearby['location'] = place['geometry']['location']
            each_nearby['type'] = place['types']
            if 'rating' in place.keys():
                each_nearby['rating'] = place['rating']
            else:
                each_nearby['rating'] = 'no rating'
            if 'link' in place.keys():
                each_nearby['link'] = place['photos'][0]['html_attributions']
            else:
                each_nearby['link'] = 'no link'
            if 'price' in place.keys():
                each_nearby['price'] = place['price_level']
            else:
                each_nearby['price'] = 'no price'
            all_nearby.append(each_nearby)
        item_dict['nearby'] = all_nearby
        each_item.append(item_dict)
    thirty_state[location] = each_item


       


t2 = datetime.datetime.now().timestamp()
save_cache(thirty_state, 'cache_all.json')
print("time with caching: ", (t2 - t1) * 1000, "ms")




