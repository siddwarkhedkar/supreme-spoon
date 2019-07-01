# Author : Sidd Warkhedkar

# Description: 
# 	1. Python script to pull Orders data from Shopify API and use Klaviyo's Server side API to track event metrics
# 	2. The script will sort through the API response (Orders data as JSON) and classify Orders as completed based on the financial_status of each
# 	3. All completed orders will be parsed to track events and create data objects for : `Placed Order` and `Ordered Product`
# 	4. Each event has the following keys : Klaviyo access token, Event Name, Customer Properties, Properties and time of occurenece as JSON objects
# 	5. The script sends base64 encoded data for each event type to the Klaviyo dashboard using the Track Events endpoint


import requests
import array
import json
import base64
import klaviyo
import time
import dateutil.parser

# Store all credentials, parameters in variables to keep the script dynamic
account = ""
shopify_key = ""
shopify_password = ""
orders_endpoint = "admin/orders.json"
date = "2016-01-01"
date_query = "?created_at_min=" + date + "T00:00:00-04:00"

# Create a url using the variables to pull data from the shopify API
shopify_url = "https://" + shopify_key + ":" + shopify_password + "@" + account + orders_endpoint + date_query
orders1 = requests.get(shopify_url) #running the curl request

# Creating a JSON object from the curl request response
orders_dump = orders1.json()

# Storing klaviyo public token necessary to track events using the Klaviyo API
klaviyo_public = ""

# Using the track endpoint to send data to Klaviyo using a get call
klaviyo_track = "https://a.klaviyo.com/api/track"

# Assumption that all orders with financial_status = paid are completed, other statuses require checking back
# Creating an empty list to store only orders which have completed status 

order3 = [] 

for i in range (0, len(orders_dump["orders"])):
	order2 = orders_dump["orders"][i]
	if order2["financial_status"] == "paid":
		order3.append(order2)

# Storing the sorted response with a similar format to the JSON response from Shopify API
orders_json = {}
orders_json["orders"]= order3

# Creating a JSON object for storing specific values based on keys and attributes Klaviyo uses to track metric events
# Using a for loop to parse through JSON object and creating the `Placed Order` event 
placed = [] 

response_placed = []

placed_urls = [] 

for i in range (0, len(orders_json["orders"])): 
    order = orders_json["orders"][i]
    obj = {}
    obj["token"] = klaviyo_public
    obj["event"] = "Placed Order"
    customer_properties = {}
    customer_properties["email"] = order["customer"]["email"]
    customer_properties["first_name"] = order["customer"]["first_name"]
    customer_properties["last_name"] = order["customer"]["last_name"]
    obj["customer_properties"] = customer_properties
    properties = {}
    properties["event_id"] = order["id"]
    properties["value"] = order["total_price"]
    properties["discount_codes"] = order["total_discounts"]
    properties["items"] = order["line_items"]
    obj["properties"] = properties
    # Converting ISO 8601 timestamp string (Shopify response) to UNIX timestamp (as required by Klaviyo) using dateutil parser and mktime function
    obj["time"] = time.mktime((dateutil.parser.parse(order['created_at'])).timetuple())
    placed.append(obj)
    obj = json.dumps(obj)
    encode_obj = str((base64.urlsafe_b64encode(obj.encode())),"utf-8")
    post_obj_url = klaviyo_track + "?data=" + encode_obj    # Create URL for every element
    placed_urls.append(post_obj_url)                        # store curls used in one variable
    response_obj = requests.get(post_obj_url)               # run curl request in for loop 
    response_placed.append(response_obj)                    # have responses for each variable 

# Creating data object for the `Ordered Product` event
product = []

response_product = []

product_urls = [] 

for i in range (0, len(orders_json["orders"])):
    order = orders_json["orders"][i]
    properties_arr = []
    for j in range (0, len(order["line_items"])):
        line_item = order["line_items"][j]
        properties1 = {}
        properties1["event_id"] = line_item["id"]
        properties1["value"] = line_item["price"]
        properties1["product_name"] = line_item["name"]
        properties1["quantity"] = line_item["quantity"]
        properties_arr.append(properties1)
    obj1 = {}
    obj1["token"] = klaviyo_public
    obj1["event"] = "Ordered Product"
    customer_properties1 = {}
    customer_properties1["email"] = order["customer"]["email"]
    customer_properties1["first_name"] = order["customer"]["first_name"]
    customer_properties1["last_name"] = order["customer"]["last_name"]
    obj1["customer_properties"] = customer_properties1
    obj1["properties"] = properties1
    obj1["time"] = time.mktime((dateutil.parser.parse(order['created_at'])).timetuple())
    product.append(obj1)
    obj1 = json.dumps(obj1)
    encode_obj1 = str((base64.urlsafe_b64encode(obj1.encode())),"utf-8")
    post_obj1_url = klaviyo_track + "?data=" + encode_obj1
    product_urls.append(post_obj1_url)
    response_obj1 = requests.get(post_obj1_url)
    response_product.append(response_obj1)

print(response_placed)
print(response_product)
