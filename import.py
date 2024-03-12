import json
import requests
import sys
import json
import requests

# Specify the path to your JSON file
# Specify the path to your JSON file
file_path = sys.argv[1]
max_iterations = int(sys.argv[2])

# Rest of the code...

# Open the JSON file
with open(file_path) as file:
    # Load the JSON data
    data = json.load(file, strict=False)

# Now you can work with the data from the JSON file
# For example, you can access specific values like this:
value = data["Addons"]

def add_catalog_item(name, data):
    # Define the URL for the API endpoint
    url = "http://localhost:8000/api/addItem"

    # Create a dictionary with the catalog item data
    catalog_item = {
        "name": name,
        "data": data
    }

    # Send a POST request to the API endpoint
    response = requests.post(url, json=catalog_item)

    # Check the response status code
    if response.status_code == 200:
        print("Catalog item added successfully")
    else:
        print("Failed to add catalog item")
    # Extract the catalog item from the response
    catalog_item = response.json()["item"]
    # Return the catalog item
    return catalog_item

def get_catalog_item(id):
    # Define the URL for the API endpoint
    url = f"http://localhost:8000/api/item/{id}"
    # Send a GET request to the API endpoint
    response = requests.get(url)
    # Check the response status code
    if response.status_code == 200:
        # Extract the catalog item from the response
        catalog_item = response.json()
        # Return the catalog item
        return catalog_item
    else:
        print("Failed to get catalog item")
        return None

def set_catalog_item(item):
    # Define the URL for the API endpoint
    url = f"http://localhost:8000/api/item/{item['id']}"
    # Send a PUT request to the API endpoint with the updated item data
    response = requests.post(url, json=item)
    # Check the response status code
    if response.status_code == 200:
        print("Catalog item updated successfully")
    else:
        print("Failed to update catalog item")

# Call the add_catalog_item function with the desired name and data
#add_catalog_item("Item Name", "Item Data")
    #print(value["name"])
    # Iterate over the key-value pairs in the data dictionary
def add_item(item, subitem):
    item["items"].append(subitem["id"])

iterations = 0
for key, value in data["Addons"].items():
    iterations += 1
    if iterations > max_iterations: break
    #print(value["name"])
    addon = add_catalog_item("addon", value["name"])
    add_item(addon, add_catalog_item("slug", value["slug"]))
    for author in value["authors"]:
        add_item(addon, add_catalog_item("author", author["name"]))
    #print(value)
    add_item(addon, add_catalog_item("addonId", key))
    add_item(addon, add_catalog_item("primaryCategoryId", value["primaryCategoryId"]))
    set_catalog_item(addon)
    print(addon)

#print(data["AddonFiles"].items())

iterations = 0
for key, value in data["AddonFiles"].items():
    iterations += 1
    if iterations > max_iterations: break
    addonfile = add_catalog_item("addonFile", value["displayName"])
    add_item(addonfile, add_catalog_item("fileName", value["fileName"]))
    add_item(addonfile, add_catalog_item("id", value["id"]))
    add_item(addonfile, add_catalog_item("addonId", value["baseAddonId"]))
    base_addon = next((item for item in data["Addons"].values() if item["id"] == int(value["baseAddonId"])), None)
    #print(base_addon)
    print("add")
    if base_addon:
        add_item(addonfile, add_catalog_item("addon", base_addon["name"]))
    set_catalog_item(addonfile)
    #print(value)