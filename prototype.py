#!/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import random
import math

class CatalogItem:
    def __init__(self, name, id, items, x, y):
        self.name = name
        self.id = id
        self.items = items
        self.x = x
        self.y = y

# Create a catalog of items
catalog = [
    CatalogItem("Item 1", 1, [], 0.5, 0.5),
    CatalogItem("Item 2", 2, [], 0, 0.5),
    CatalogItem("Item 3", 3, [], -0.5, 0),
]

def generate_new_id():
    # Find the maximum id in the catalog
    max_id = max(item.id for item in catalog)
    # Generate a new id by incrementing the maximum id
    new_id = max_id + 1
    return new_id

def generate_unique_coordinates(c_x, c_y, distance, tolerance=0.1):
    attempts = 0
    while True:
        # Generate random x and y coordinates within the specified distance
        x = c_x + random.uniform(-distance, distance)
        y = c_y + random.uniform(-distance, distance)
        
        # Check if the generated coordinates are within the specified distance to c_x and c_y
        if (math.sqrt((x - c_x) ** 2 + (y - c_y) ** 2) > distance):
            continue

        # Check if the generated coordinates are unique
        is_unique = True
        for item in catalog:
            # Calculate the distance between the generated coordinates and the existing item coordinates
            distance_between_items = math.sqrt((x - item.x) ** 2 + (y - item.y) ** 2)

            # If the distance is less than the specified distance, the coordinates are not unique
            if distance_between_items < tolerance:
                is_unique = False
                break
        
        # If the coordinates are unique, return them
        if is_unique:
            return x, y
        
        attempts += 1
        if attempts > 100:
            return x, y


def get_catalog_item(id):
    return next((item for item in catalog if item.id == id), None)

def get_catalog_vector_for_name(name):
    # Get the average vector coordinate for all items with name
    items = [item for item in catalog if item.name == name]
    if items:
        # Calculate the average x and y coordinates
        c_x = sum(item.x for item in items) / len(items)
        c_y = sum(item.y for item in items) / len(items)
        return c_x, c_y
        #return items[0].x, items[0].y
    else:
        #return generate_unique_coordinates(0,0,1.0, 0.5)
        # Convert the name to a number
        #name_number = sum(ord(char) for char in name)
        # Calculate the x and y coordinates using sin and cos
        theta = random.uniform(0, 2 * math.pi)
        x = math.sin(theta)
        y = math.cos(theta)
        return x, y

def get_catalog_vector(name):
    # Get the average vector coordinate for new item
    weight = 0.8
    x, y = get_catalog_vector_for_name(name)
    return generate_unique_coordinates(x,y,1 - weight, 0.01)


def add_catalog_item(name):
    # Generate a new id for the catalog item
    new_id = generate_new_id()
    # Create a new catalog item
    x, y = get_catalog_vector(name)
    # Check if any items in the catalog match the given name and data
    matching_items = [item for item in catalog if item.name == name]

    # If there is a matching item, return it
    if matching_items:
        return matching_items[0]

    # Otherwise, continue with adding the new item to the catalog
    new_item = CatalogItem(name, new_id, [], x, y)
    # Add the new item to the catalog
    catalog.append(new_item)
    
    return new_item

def change_catalog_item(id, name):
    # Find the item with the given id in the catalog
    item = next((item for item in catalog if item.id == id), None)
    if item:
        # Update the item fields with the input data
        item.name = name
        return item
    else:
        return None

def calculate_vector_coordinates(item):
    # Base case: if the item has no items, return its own coordinates
    if not item.items:
        return get_catalog_vector(item.name)
    
    # Recursive case: calculate the coordinates of all the items within the item
    #sub_coordinates = [calculate_vector_coordinates(get_catalog_item(sub_item)) for sub_item in item.items]
    sub_coordinates = [get_catalog_vector(get_catalog_item(sub_item).name) for sub_item in item.items]

    c_x = sum(x for x, y in sub_coordinates) / len(sub_coordinates)
    c_y = sum(y for x, y in sub_coordinates) / len(sub_coordinates)

    return c_x, c_y

def get_first_order_items():
    # Get all the items that are not items of any other items
    first_order_items = [item for item in catalog if len(item.items) < 1]
    return first_order_items

def get_child_items(id):
    # Find the item with the given id in the catalog
    item = next((item for item in catalog if item.id == id), None)
    if item:
        # Get all the items that are items of the given item
        child_items = [get_catalog_item(child_item) for child_item in item.items]
        return child_items
    else:
        return None

# Define the request handler class
class MyRequestHandler(BaseHTTPRequestHandler):
    # Update the do_GET method to handle serving catalog items by id
    def do_GET(self):
        if not self.path.startswith('/api/'):
            try:
                # Open the requested file
                if self.path.endswith('/'):
                    self.path += 'index.html'
                with open('.' + self.path, 'rb') as file:
                    # Send response status code
                    self.send_response(200)
                    # Determine the content type based on the file extension
                    if self.path.endswith('.html'):
                        content_type = 'text/html'
                    elif self.path.endswith('.css'):
                        content_type = 'text/css'
                    elif self.path.endswith('.js'):
                        content_type = 'application/javascript'
                    else:
                        content_type = 'application/octet-stream'
                    # Send headers
                    self.send_header('Content-type', content_type)
                    self.end_headers()
                    # Send response body
                    self.wfile.write(file.read())
            except FileNotFoundError:
                # Send response status code
                self.send_response(404)
                # Send headers
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                # Send response body
                response = {'message': 'File not found'}
                self.wfile.write(json.dumps(response).encode())
        if self.path.startswith('/api/'):
            if self.path.startswith('/api/item/'):
                # Extract the item id from the path
                item_id = int(self.path.split('/')[-1])
                # Find the item with the given id in the catalog
                item = next((item for item in catalog if item.id == item_id), None)
                if item:
                    # Send response status code
                    self.send_response(200)
                    # Send headers
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    # Send response body
                    response = {'item': item.__dict__}
                    self.wfile.write(json.dumps(response).encode())
                else:
                    # Send response status code
                    self.send_response(404)
                    # Send headers
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    # Send response body
                    response = {'message': 'Item not found'}
                    self.wfile.write(json.dumps(response).encode())
            elif self.path.startswith('/api/child_items/'):
                item_id = int(self.path.split('/')[-1])
                # Find the item with the given id in the catalog
                item = next((item for item in catalog if item.id == item_id), None)
                if item:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'items': [item.__dict__ for item in get_child_items(item_id)]}
                    self.wfile.write(json.dumps(response).encode())
                else:
                    # Send response status code
                    self.send_response(404)
                    # Send headers
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    # Send response body
                    response = {'message': 'Item not found'}
                    self.wfile.write(json.dumps(response).encode())                    
            elif self.path == '/api/items':
                # Send response status code
                self.send_response(200)
                # Send headers
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                # Send response body
                response = {'items': [item.__dict__ for item in catalog]}
                self.wfile.write(json.dumps(response).encode())
            elif self.path == '/api/first_order_items':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = { 'items': [item.__dict__ for item in get_first_order_items()]}
                self.wfile.write(json.dumps(response).encode())
        

    # Update the do_POST method to handle adding new catalog items
    def do_POST(self):
        if self.path == '/api/addItem':
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Parse the JSON data
            json_data = json.loads(post_data)

            # Create a new catalog item
            new_item = add_catalog_item(json_data['name'])

            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Send response body
            response = {'message': 'POST request received', 'item': new_item.__dict__}
            self.wfile.write(json.dumps(response).encode())
        elif self.path.startswith('/api/item/'):
            # Extract the item id from the path
            item_id = int(self.path.split('/')[-1])
            # Find the item with the given id in the catalog
            item = next((item for item in catalog if item.id == item_id), None)
            if item:
            # Read the request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')

                # Parse the JSON data
                json_data = json.loads(post_data)

                # Update all fields of the item with the input data
                item.name = json_data['name']
                item.id = json_data['id']
                if json_data['items'] and len(json_data['items']) > 0:
                    item.items = list(set(json_data['items']))
                item.x, item.y = calculate_vector_coordinates(item)

                # Send response status code
                self.send_response(200)

                # Send headers
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                # Send response body
                response = {'message': 'POST request received', 'item': item.__dict__}
                self.wfile.write(json.dumps(response).encode())
            else:
                # Send response status code
                self.send_response(404)
                # Send headers
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                # Send response body
                response = {'message': 'Item not found'}
                self.wfile.write(json.dumps(response).encode())

# Create an HTTP server instance
server = HTTPServer(('localhost', 8000), MyRequestHandler)

# Start the server
server.serve_forever()