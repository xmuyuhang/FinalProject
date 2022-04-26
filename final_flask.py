#final_flask.py
import requests
import json
import webbrowser
import plotly.graph_objs as go
import plotly.express as px
from flask import Flask, render_template, request
import pandas as pd
from collections import Counter
########################################
#### Part1: Prepare for a tree
########################################
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
            this_rate = node.data['rating']
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

########################################
#### Part2: Setting for using Cache 
########################################
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


###################################
#### Part3: Prepare data for plotly
###################################
def get_data(state):
    list_name = []
    list_rating = []
    list_price = []
    data = open_cache("cache_all.json")[state]
    for item in data:
        list_rating.append(item['rating'])
        list_price.append(item['price'])
        list_name.append(item['name'])
    return list_rating, list_price, list_name

##################################
#### Part4: Read json for 30 trees
##################################
data = open_cache("cache_trees.json")
city_tree_dict={}
for city in data:
    city_tree=Tree(city)
    city_tree.read_tree_json(data[city])
    city_tree_dict[city]=city_tree


detail_nb = open_cache('nb_detail.json')

######################
#### Part5: Flask app
######################
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('FlaskP1.html')

@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    global fave_state
    fave_state = request.form["state"]
    list_rating, list_price, list_name = get_data(fave_state)
    r = Counter(list_rating)
    df_r = pd.DataFrame.from_dict(r, orient='index').reset_index()
    df_r.columns = ['rating','number']
    df_r = df_r.sort_values(by="rating")
    d = Counter(list_price)
    df = pd.DataFrame.from_dict(d, orient='index').reset_index()
    df.columns = ['price','number']
    df = df.sort_values(by="price")
    fig1 = px.histogram(df_r, x='rating', y='number', title='the Distribution of Rating')
    fig1.update_layout(title_x=0.5, width=500)
    fig1.update_layout(yaxis_title="Count")
    fig2 = px.histogram(df, x='price', y='number', title='the Distribution of Price')
    fig2.update_layout(title_x=0.5, width=500)
    fig2.update_layout(yaxis_title="Count")
    div1 = fig1.to_html(full_html=False)
    div2 = fig2.to_html(full_html=False)
    
    return render_template('response.html', state=fave_state, plot_div1=div1, plot_div2=div2)


@app.route('/results', methods=['POST'])
def handle_the_form2():
    global info
    fave_rating = request.form.get('rating', type=float)
    fave_price = request.form["price"]
    info = city_tree_dict[fave_state].tree2inorder_print(fave_rating, fave_price)
    if info:
        results_or_not = '1'
        data_rating = []
        data_price = []
        data_type = []
        res_info = []
        for item in info:
            data_rating.append(item['rating'])
            data_price.append(item['price'])
            data_type.append(item['type'])
            res_info.append((item['name'], item['rating'], item['price'], item['type']))
        data_price = list(map(int, data_price))
        aver_rate = sum(data_rating)/len(data_rating)
        aver_price = sum(data_price)/len(data_price)
        xvals = ['rating', 'price']
        yvals = [aver_rate, aver_price]
        bar_data = go.Bar(x=xvals, y=yvals)
        basic_layout = go.Layout(title="A Bar Graph")
        fig = go.Figure(data=bar_data, layout=basic_layout)
        fig.update_layout(title_text='A Bar Graph of Average Ratings and Prices', title_x=0.5, width=700)
        fig.update_layout(yaxis_title="Count")
        div = fig.to_html(full_html=False)
        d = Counter(data_type)
        df = pd.DataFrame.from_dict(d, orient='index').reset_index()
        fig2 = px.pie(df,names="index",values=0)
        fig2.update_layout(title={
            "text":"the Percentage of Different Types of Restaurants",
            "y":0.96, 
            "x":0.5,  
            "xanchor":"center",
            "yanchor":"top"  
            }
            )
        div2 = fig2.to_html(full_html=False)
    else:
        results_or_not = '0'
        div = None
        div2 = None
        res_info = None
    



    return render_template('FlaskP3.html', results_or_not=results_or_not, plot_div=div, results=res_info, plot_div2=div2)

@app.route('/details', methods=['POST'])
def handle_the_form3():
    name = request.form["specify"]
    for item in info:
        if name in item['name']:
            spec_info = item
            nb_res = item['nearby']

    nb = []
    for item in nb_res:
        nb_dict = {}
        if 'name' in detail_nb[item['name']].keys():
            nb_dict['name'] = detail_nb[item['name']]['name']
        else:
            nb_dict['name'] = 'unfounded'
        if 'rating' in detail_nb[item['name']].keys():
            nb_dict['rating'] = detail_nb[item['name']]['rating']
        else:
            nb_dict['rating'] = 'unfounded'
        if 'formatted_address' in detail_nb[item['name']].keys():
            nb_dict['address'] = detail_nb[item['name']]['formatted_address']
        else:
            nb_dict['address'] = 'unfounded'
        if 'formatted_phone_number' in detail_nb[item['name']].keys():
            nb_dict['phone'] = detail_nb[item['name']]['formatted_phone_number']  
        else:
            nb_dict['phone'] = 'unfounded'
        if 'website' in detail_nb[item['name']].keys():
            nb_dict['website'] = detail_nb[item['name']]['website']  
        else:
            nb_dict['website'] = 'unfounded'
        nb.append(nb_dict)
    

    nb_info = []
    for item in nb:
        nb_info.append((item['name'], item['rating'], item['address'], item['phone'], item['website']))

    for idx,item in enumerate(nb_info):
        if name in item[0]:
            nb_info.pop(idx)

        


    return render_template('FlaskLast.html', spec_info=spec_info, nearby_info=nb_info, nb_city=fave_state)

if __name__ == "__main__":
    app.run(debug=True) 
