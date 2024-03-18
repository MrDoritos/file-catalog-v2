#!/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random
import math

from httplib2 import ServerNotFoundError

class CatalogItem:
    def __init__(self, name, id, parents, children, x, y):
        self.name = name
        self.id = id
        self.parents = parents
        self.children = children
        self.x = x
        self.y = y

    def addItem(self, item, array):
        if item.id not in array:
            array.append(item.id)

    def removeItem(self, item, array):
        if item.id in array:
            array.remove(item.id)

    def addParent(self, parent):
        self.addItem(parent, self.parents)
        parent.addChild(self) 
        
    def addChild(self, child):
        self.addItem(child, self.children)
        child.addParent(self)

    def removeParent(self, parent):
        self.removeItem(parent, self.parents)
        parent.removeChild(self)

    def removeChild(self, child):
        self.removeItem(child, self.children)
        child.removeParent(self)

class Index:
    def __init__(self):
        self.catalog = []

    def getItem(self, id):
        return next((item for item in self.catalog if item.id == id), None)
    
    def hasItem(self, id):
        return self.getItem(id) != None
    
    def getItemByName(self, name):
        return next((item for item in self.catalog if item.name == name), None)

    def hasItemByName(self, name):
        return self.getItemByName(name) != None

    def generateId(self):
        if not self.catalog or len(self.catalog) == 0:
            return 0
        max_id = max(item.id for item in self.catalog)
        new_id = max_id + 1
        return new_id

    def generateUniqueCoords(self, c_x, c_y, distance, tolerance=0.1):
        attempts = 0
        while True:
            x = c_x + random.uniform(-distance, distance)
            y = c_y + random.uniform(-distance, distance)

            if (math.sqrt((x - c_x) ** 2 + (y - c_y) ** 2) > distance):
                continue

            is_unique = True
            for item in self.catalog:
                distance_between_items = math.sqrt((x - item.x) ** 2 + (y - item.y) ** 2)
                if distance_between_items < tolerance:
                    is_unique = False
                    break
            if is_unique:
                return x, y
            attempts += 1
            if attempts > 100:
                return x, y

    def getVector(self, name):
        items = [item for item in self.catalog if item.name == name]
        c_x, c_y = 0, 0
        if items:
            c_x = sum(item.x for item in items) / len(items)
            c_y = sum(item.y for item in items) / len(items)
        else:
            theta = random.uniform(0, 2 * math.pi)
            c_x = math.sin(theta)
            c_y = math.cos(theta)
        
        weight = 0.2
        return self.generateUniqueCoords(c_x, c_y, weight, 0.01)
            
    def calculateVector(self, item):
        if not item.children:
            return self.getVector(item.name)
        
        sub_coordinates = [self.getVector(self.getItem(child).name) for child in item.children]

        c_x = sum(x for x, y in sub_coordinates) / len(sub_coordinates)
        c_y = sum(y for x, y in sub_coordinates) / len(sub_coordinates)

        return c_x, c_y

    def addItem(self, name):
        new_id = self.generateId()
        x, y = self.getVector(name)

        if (self.hasItemByName(name)):
            return self.getItemByName(name)
        
        new_item = CatalogItem(name, new_id, [], [], x, y)
        
        self.catalog.append(new_item)

        return new_item
    
    def addOrGetItemByName(self, name):
        if (self.hasItemByName(name)):
            return self.getItemByName(name)
        else:
            return self.addItem(name)
        
    def modifyOrAddItem(self, item):
        if (self.hasItem(item.id)):
            old_item = self.getItem(item.id)
            c_i = self.catalog.index(old_item)
            self.catalog[c_i] = item
        else:
            self.catalog.append(item)
        return item

    def getChildItems(self, item):
        return [self.getItem(child) for child in item.children]
    
    def getParentItems(self, item):
        return [self.getItem(parent) for parent in item.parents]

    def getFirstOrderItems(self):
        return [item for item in self.catalog if not item.parents]
    
class APIRequestHandler(BaseHTTPRequestHandler):
    def serve_file(self):
        if self.path.endswith('/'):
            self.path += 'index.html'
        try:
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

    def parse_json(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        return json.loads(post_data)

    def get_item_from_index(self):
        item = self.get_item_from_client()

        if (self.index.hasItem(item.id)):
            return self.index.getItem(item.id)
        
        if (self.index.hasItemByName(item.name)):
            return self.index.getItemByName(item.name)
        
        return None
        
    def get_item_from_client(self):
        json_data = self.parse_json()
        item = CatalogItem(json_data['name'], 
                           json_data['id'], 
                           json_data['parents'], 
                           json_data['children'], 
                           json_data['x'], 
                           json_data['y'])
        return item

    def get_item(self):
        item = None

        if self.path in self.clientItem:
            item = self.get_item_from_client()
        elif self.path in self.indexItem:
            item = self.get_item_from_index()

        return item

    def serve_notfound(self):
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'message': 'Item not found'}
        self.wfile.write(json.dumps(response).encode())

    def serve_items(self, items):
        if not items:
            return self.serve_notfound()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = {'message': 'No items', 'item': {}}

        print(items)

        if len(items) == 1:
            response = {'message': 'Item success', 'item': items[0]}
        else:
            response = {'message': 'Items success', 'items': items}
        
        self.wfile.write(json.dumps(response, default=lambda o: o.__dict__).encode())

    def serve_vector(self, x, y):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'message': 'Vector success', 'x': x, 'y': y}
        self.wfile.write(json.dumps(response).encode())

    def serve_api_index_get(self):
        items = []

        match self.path:
            case '/api/index/getItems':
                items = index.catalog
            case '/api/index/getFirstOrderItems':
                items = index.getFirstOrderItems()

        return self.serve_items(items)

    def serve_api_index_post(self):
        item = self.get_item()
        items = []

        if not item:
            return self.serve_notfound()

        match self.path:
            case '/api/index/getItem':
                items.append(item)
            case '/api/index/addItem':
                items.append(index.addItem(item.name))
            case '/api/index/modifyItem':
                items.append(index.modifyOrAddItem(item))
            case '/api/index/addOrGetItem':
                items.append(index.addOrGetItemByName(item.name))
            case '/api/index/getChildItems':
                items = index.getChildItems(item)
            case '/api/index/getParentItems':
                items = index.getParentItems(item)
            case '/api/index/getVector':
                x, y = index.getVector(item.name)
                return self.serve_vector(x, y)
            case '/api/index/calculateVector':
                x, y = index.calculateVector(item)
                return self.serve_vector(x, y)
            case '/api/index/getItemRange':
                json_data = self.parse_json()

        return self.serve_items(items)        

    def serve_api_catalogitem_get(self):
        return

    def serve_api_catalogitem_post(self):
        return

    def serve_api_get(self):
        if self.path.startswith('/api/index'):
            self.serve_api_index_get()
        if self.path.startswith('/api/catalogitem'):
            self.serve_api_catalogitem_get()

    def serve_api_post(self):
        if self.path.startswith('/api/index'):
            self.serve_api_index_post()
        if self.path.startswith('/api/catalogitem'):
            self.serve_api_catalogitem_post()

    def do_GET(self):
        if not self.path.startswith('/api'):
            self.serve_file()

        if self.path.startswith('/api'):
            self.serve_api_get()

    def do_POST(self):
        if self.path.startswith('/api'):
            self.serve_api_post()

    clientItem = [
        '/api/index/addItem',
        '/api/index/modifyItem',
        '/api/index/addOrGetItem',
    ]
    indexItem = [
        '/api/index/getItem',
        '/api/index/getChildItems',
        '/api/index/getParentItems',
        '/api/index/getVector',
        '/api/index/calculateVector',
    ]
    noItem = [
        '/api/index/getFirstOrderItems',
        '/api/index/getItems',
        '/api/index/getItemRange'
    ]
        
index = Index()
for i in range(ord('A'), ord('Z')+1):
    name = chr(i)
    index.addItem(name)
server = HTTPServer(('localhost', 8000), APIRequestHandler)
server.serve_forever()