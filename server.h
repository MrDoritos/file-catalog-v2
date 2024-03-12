#pragma once

#include "httplib.h"
#include "catalog.h"

class Server {
public:
    Server(int port, Catalog& catalog);
    void start();

private:
    httplib::Server svr;
    Catalog& catalog;

    void handleGetItem(const httplib::Request& req, httplib::Response& res);
    void handleAddItem(const httplib::Request& req, httplib::Response& res);
    void handleUpdateItem(const httplib::Request& req, httplib::Response& res);
};