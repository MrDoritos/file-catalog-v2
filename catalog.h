#pragma once

#include <unordered_map>
#include <vector>
#include <string>

class CatalogItem;

class Catalog {
public:
    CatalogItem& getItem(long id);
    void addItem(const std::string& name, const std::vector<char>& data);
    void updateItem(long id, const std::string& name, const std::vector<char>& data);

private:
    std::unordered_map<long, CatalogItem> items;
    long nextId;
};