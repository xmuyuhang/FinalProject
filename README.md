# SI507_finalproject

This is a project about searching for restaurants in top thirty cities by population in U.S. Users could choose any city of that and select the rating and price they prefer. Finally, they could see more detail information of one restaurant in the last page and some information of nearby restaurants.
# Data Structure
I use tree as the main data structure(in cache_trees.json).

I organize my data into 30 trees according to different cities. Besides, in each tree, I order the tree according to the level of rating, which means a restaurant with higher level of rating will be put in right child and a restaurant with lower level of rating will be put in left child. If there are two restaurants with the same level of rating, I will compare level of price of them. In this case, a restaurant with higher level of price will be put in right child and a restaurant with lower level of price will be put in left child.

# How to running the code
# Step1: Get your API keys and put them in secrets.py
In order to run the code, you need to get your own API keys from YELP and Google Maps.

The website for you to get YELP API Key: https://www.yelp.com/developers/documentation/v3/authentication
(click "Create App", follow their instructions and get your API key!)

The website for you to get Google Maps API Key: https://developers.google.com/maps/documentation/javascript/get-api-key#creating-api-keys (follow their instructions and get your API key!). 

Once you get API keys, make secret.py in the same folder with your project code and save the API key in secret.py.  The secret.py file should contain this (replace “xxxxxxx” with your API key): 

YELP_API_KEY = xxxxxxx

GOOGLE_API_KEY = xxxxxxx

# Step2: Install Python Packages
Please install the Python packages for my project to work first:
NumPy, Plotly, Flask, Requests, Pandas, tqdm, datetime, collections.

# Step3: Run the final_project.py
This program was made by Flask app, please run the final_flask.py locally:
python final_flask.py

Then open http://127.0.0.1:5000/ in your browser.
# Step 4: Interact with the program
After open the http://127.0.0.1:5000/ , you could find an website. You could select the city you want to visit in the box. Click on “Submit!” and you will get to a new page. 

In this new page, you could see two histograms describing the distribution of ratings and prices of all restaurants in this city. You could choose the level of rating and price you prefer and click on “Search!” and you will get to a new page.

The new page offers you a bar chart of the average rating and price of the restaurants meeting with your request before and one pie chart about the percentage of different types of these restaurants. You could also see a table containing some information of these restaurants. You could choose any restaurant you want to look into in the box, and then click "Submit!"

At the last page, you could see the more details information about this restaurant including its phone, address, website and so on. It also provides some information of other restaurants nearby this restaurant for you.




