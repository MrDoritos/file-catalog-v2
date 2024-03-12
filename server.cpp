#include "server.h"

Server::Server(int port, Catalog& catalog)
    : svr(), catalog(catalog) {
    svr.Get("/items/:id", [this](const httplib::Request& req, httplib::Response& res) {
        handleGetItem(req, res);
    });
    svr.Post("/items", [this](const httplib::Request& req, httplib::Response& res) {
        handleAddItem(req, res);
    });
    svr.Put("/items/:id", [this](const httplib::Request& req, httplib::Response& res) {
        handleUpdateItem(req, res);
    });
}

void Server::start() {
    svr.listen("0.0.0.0", 8080);
}

void Server::handleGetItem(const httplib::Request& req, httplib::Response& res) {
    // Implement logic to retrieve and return a CatalogItem
}

void Server::handleAddItem(const httplib::Request& req, httplib::Response& res) {
    // Implement logic to add a new CatalogItem
}

void Server::handleUpdateItem(const httplib::Request& req, httplib::Response& res) {
    // Implement logic to update an existing CatalogItem
}