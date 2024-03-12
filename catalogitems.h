#include <string>
#include <vector>

/*
The CatalogItem datatype
*/
struct CatalogItem {
    std::string name;
    long id;
    const char *data;
    std::vector<CatalogItem*> references;
};

/*
Stores and manages a collection of CatalogItems.
Holds singleton instance of Index
*/
struct Index {
    Index() {
        puts("New Index instance");
        instance = this;
        items = std::vector<CatalogItem*>(1);
    }
    static Index *instance;
    std::vector<CatalogItem*> items;

    CatalogItem* getItem(long id) {
        for (auto* item : items) {
            if (item->id == id) {
                return item;
            }
        }
        return nullptr;
    }

    CatalogItem* getItem(const std::string& name) {
        for (auto* item : items) {
            if (item->name == name) {
                return item;
            }
        }
        return nullptr;
    }

    void addItem(CatalogItem* item) {
        // Check if an item with the same id already exists
        for (auto* existingItem : items) {
            if (existingItem->id == item->id) {
                return; // Item with the same id already exists, do not add
            }
        }

        // Add the item to the items vector
        items.push_back(item);
    }

    CatalogItem* createItem(std::string name, const char* data) {
        puts("Create item(s,s)");
        CatalogItem* newItem = createItem();
        newItem->name = name;
        newItem->data = data;
        return newItem;
    }

    CatalogItem* createItem() {
        puts("Create item");
        long nextId = 0;
        for (const auto* item : items) {
            if (item->id >= nextId) {
                nextId = item->id + 1;
            }
        }
        printf("Next id: %ld\n", nextId);
        CatalogItem *newItem = new CatalogItem();
        newItem->id = nextId;
        items.push_back(newItem);
        puts("Create item end");
        return items.back();
    }
};

Index *Index::instance = nullptr;