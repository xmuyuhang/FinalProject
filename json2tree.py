#########################################
##### Name: Yuhang Zheng            #####
##### Uniqname: zyuhang             #####
#########################################

import requests
import json
import webbrowser
from collections import Counter
import pandas as pd
import plotly.express as px

CACHE_FILENAME = "cache_all.json"
SAVE_CACHE_FILENAME = "cache_trees.json"
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

def save_cache(cache_dict):
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
    fw = open(SAVE_CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()

class Tree:
    def __init__(self,city):
        self.city=city
        self.root=None
    def insert_node(self,new_data):
        if self.root==None:
            self.root=Node(new_data)
        else:
            self._put(new_data,self.root)
    def _put(self,new_data,current_node):
        if new_data['rating'] < current_node.data['rating']:
            if current_node.has_left_child():
                self._put(new_data, current_node.left)
            else:
                current_node.insert_left(Node(new_data))
        elif new_data['rating'] == current_node.data['rating']:
            if new_data['price'] < current_node.data['price']:
                if current_node.has_left_child():
                    self._put(new_data, current_node.left)
                else:
                    current_node.insert_left(Node(new_data))
            else:
                if current_node.has_right_child():
                    self._put(new_data,current_node.right)
                else:
                    current_node.insert_right(Node(new_data)) 
        else:
            if current_node.has_right_child():
                self._put(new_data,current_node.right)
            else:
                current_node.insert_right(Node(new_data)) 
        
    def tree2preorder_list(self):
        return self._tree2preorder_list(self.root)
    
    def tree2inorder_print(self,rate_threshold,price_threshold):
        return self._tree2inorder_print(self.root,rate_threshold,price_threshold)


    def _tree2preorder_list(self,node):
        if node==None:
            return []
        tree_list=[]
        tree_list.extend([node.data])
        tree_list.extend(self._tree2preorder_list(node.left))
        tree_list.extend(self._tree2preorder_list(node.right))
        return tree_list
    
    def _tree2inorder_print(self,node,rate_threshold,price_threshold):
        results=[]
        if node:
            this_rate=node.data['rating']
            this_price = node.data['price']
            results.extend(self._tree2inorder_print(node.left,rate_threshold,price_threshold))
            if this_rate>=rate_threshold and this_price>=price_threshold:
                results.append(node.data)
            results.extend(self._tree2inorder_print(node.right,rate_threshold,price_threshold))
        return results
    
    def print_tree(self):
        self._print_tree(self.root)
    def _print_tree(self,node):
        if node==None:
            return
        self._print_tree(node.left)
        print(node.data)
        self._print_tree(node.right)

    def tree2json(self):
        return self._tree2json(self.root)

    def _tree2json(self,node):
        node_dict={}
        if node.left is not None:
            node_dict['left']=self._tree2json(node.left)
        node_dict['data']=node.data
        if node.right is not None:
            node_dict['right']=self._tree2json(node.right)
        return node_dict

    def read_tree_json(self,json_dict):
        self.root = self._read_tree_json(json_dict)

    def _read_tree_json(self,json_dict):
        node=Node(json_dict['data'])
        if 'left' in json_dict:
            node.left=self._read_tree_json(json_dict['left'])
        if 'right' in json_dict:
            node.right=self._read_tree_json(json_dict['right'])
        return node


    

class Node:
    def __init__(self, data):
        self.data = data
        self.left=None
        self.right=None
    
    def has_left_child(self):
        return not (self.left==None)
    
    def has_right_child(self):
        return not (self.right==None)

    def insert_left(self, child):
        self.left=child

    def insert_right(self, child):
        self.right=child



# read from tree json
data = open_cache(SAVE_CACHE_FILENAME)
city_tree_dict={}
for city in data:
    city_tree=Tree(city)
    city_tree.read_tree_json(data[city])
    city_tree_dict[city]=city_tree

print one tree
city_tree_dict['New York'].print_tree()
