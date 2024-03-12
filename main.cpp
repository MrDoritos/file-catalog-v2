#include "catalogitems.h"
#include <boost/asio.hpp>
#include <boost/beast.hpp>

int main() {
    // Initialize the catalog
    
    // Create and start the server
    boost::asio::io_context io_context;
    boost::asio::ip::tcp::acceptor acceptor(io_context, boost::asio::ip::tcp::endpoint(boost::asio::ip::tcp::v4(), 8080));

    while (true) {
        #include <boost/beast/http.hpp> // Include the necessary header file
        

        boost::asio::ip::tcp::socket socket(io_context);
        acceptor.accept(socket);

        boost::beast::http::request<boost::beast::http::string_body> request;
        boost::beast::http::read(socket, request);

        // Process the request and generate a response using the catalog

        boost::beast::http::response<boost::beast::http::string_body> response;
        response.version(request.version());
        response.result(boost::beast::http::status::ok);
        response.set(boost::beast::http::field::server, "Boost Beast Server");
        response.set(boost::beast::http::field::content_type, "text/plain");
        response.body() = "Hello, World!";
        response.prepare_payload();

        boost::beast::http::write(socket, response);
    }

    return 0;
}