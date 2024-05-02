#include <string>
#include <vector>

using namespace std;

struct Link {
    Link(string name) {
        this->name = name;
    }
    string name;
};

struct Chain : Link {
    Chain(string name) : Link(name) {
        this->name = name;
    }
    vector<Link*> links;
};

struct Locker {
    vector<Chain*> chains;
};