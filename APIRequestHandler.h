#pragma once

#include <boost/beast/core.hpp>
#include <boost/beast/http.hpp>
#include <boost/beast/version.hpp>
#include <boost/asio/dispatch.hpp>
#include <boost/asio/strand.hpp>
#include <boost/beast/http/message.hpp>
#include <boost/config.hpp>

namespace beast = boost::beast;         // from <boost/beast.hpp>
namespace http = beast::http;           // from <boost/beast/http.hpp>
namespace net = boost::asio;            // from <boost/asio.hpp>
using tcp = boost::asio::ip::tcp;       // from <boost/asio/ip/tcp.hpp>

#include "catalogitems.h"

template <class Body, class Allocator>
struct APIRequestHandler : public Index {
    static APIRequestHandler *instance;

    //add from multipart data
    CatalogItem* AddCatalogItem(beast::string_view doc_root, http::request<Body, http::basic_fields<Allocator>> req) {
        return nullptr;
    }

    //get from id in api url
    CatalogItem* GetCatalogItem(beast::string_view doc_root, http::request<Body, http::basic_fields<Allocator>> req) {
        // Get the URL path
        std::string path = req.target().to_string();

        // Find the last '/' character in the path
        std::size_t lastSlashPos = path.rfind('/');
        if (lastSlashPos != std::string::npos) {
            // Extract the id from the path
            std::string id = path.substr(lastSlashPos + 1);

            // Convert the id to an integer if needed
            int idValue = std::stoi(id);

            // Use the idValue as needed
            // ...
            return getItem(idValue);
        }

        return nullptr;
    }

    // /api/add
    // /api/get/{num}
    // /api/set/{num}
    // 

    void Add_Test_Data() {
        puts("Adding test data");
        createItem("tag", "apple");
        createItem("color", "red");
        createItem("taste", "sweet");
        createItem("file", "apple_data");
        createItem("filename", "apple.png");
        /*
        file - data
         | tag - apple
         | color - red
            | wavelength - 650nm
         | taste - sweet
            | chemical - sugar
         | filename - apple.png
         | colorspace - srgb
         | hash - 1234567890
            | sha256 - 1234567890abcdef
            | mda5 - 1234567890abcdef
         | id - 01
         | date - 2021-01-01
            | year - 2021
            | month - 01
                | name - january
            | day - 01
            | day - tuesday
         | - time - 12:00:00
        
        */
    }

    http::response<http::string_body> GetResponse(beast::string_view doc_root,
            http::request<Body, http::basic_fields<Allocator>> req) {
            http::response<http::string_body> res{http::status::internal_server_error, req.version()};
            res.set(http::field::server, BOOST_BEAST_VERSION_STRING);
            res.set(http::field::content_type, "text/html");
            res.keep_alive(req.keep_alive());

            // Check if the request is for /api/add_test_data
            if (req.target() == "/api/add_test_data") {
                // Call the Add_Test_Data() function
                Add_Test_Data();
                res.result(http::status::ok);
                res.body() = "Test data added";
            } 
            // Check if the request is for /api/get/{num}
            else if (req.target().starts_with("/api/get/")) {
                // Extract the id from the path
                std::string path = req.target();
                std::string id = path.substr(9); // Remove "/api/get/" from the path

                // Convert the id to an integer if needed
                int idValue = std::stoi(id);

                // Get the CatalogItem with the specified id
                CatalogItem* item = getItem(idValue);

                if (item) {
                    // Create the response body with the CatalogItem name
                    res.result(http::status::ok);
                    res.body() = item->name;
                } else {
                    // CatalogItem not found
                    res.result(http::status::not_found);
                    res.body() = "CatalogItem not found";
                }
            }
            else {
                res.result(http::status::not_found);
                res.body() = "API not implemented";
            }

            res.prepare_payload();
            return res;
        }

};

template<class Body, class Allocator>
APIRequestHandler<Body, Allocator>* APIRequestHandler<Body, Allocator>::instance;
