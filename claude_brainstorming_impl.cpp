#include <vector>
#include <string>
#include <algorithm> 

struct Node;

struct ReferenceNode {
    ReferenceNode() {
        reference = nullptr;
    }
    ReferenceNode(Node* ref) {
        reference = ref;
    }

    Node* reference;
};

struct ChildNode : ReferenceNode {
    ChildNode()
    :ReferenceNode() {
        weight = 1.0;
    }
    ChildNode(ReferenceNode ref, float weight) 
    :ReferenceNode(ref) {
        this->weight = weight;
    }

    float weight;
};

struct Node {
    Node() {
        name = defaultName;
    }
    Node(std::string name) {
        this->name = name;
    }

    std::vector<ReferenceNode> parents;
    std::vector<ChildNode> children;

    const static std::string defaultName;
    std::string name;
};

const std::string Node::defaultName = "undefined node";

struct Environment {
    std::vector<Node> root_nodes;
    std::vector<Node> all_nodes;

    void addToList(std::vector<Node*>* vec, Node *node) {
        if (std::count(vec->begin(), vec->end(), node) < 1) {
            vec->push_back(node);
        }
        for (const ChildNode& childNode : node->children) {
            addToList(vec, childNode.reference);
        }
    }

    ReferenceNode findNode(std::string name) {
        if (!nodeExists(name))
            return ReferenceNode();
        
        for (int i = 0; i < all_nodes.size(); i++) {
            if (all_nodes[i].name == name) {
                return ReferenceNode(&all_nodes[i]);
            }
        }
    }

    void putNode(ReferenceNode candidate) {
        ReferenceNode envrn = findNode(candidate.reference->name);

        if (envrn.reference == nullptr) {
            all_nodes.push_back(*candidate.reference);
            root_nodes.push_back(*candidate.reference);
            return;
        }

        if (candidate.reference->parents.size() > 0) {
            if (count(root_nodes.begin(), root_nodes.end(), candidate.reference) > 0) {
                root_nodes.erase(std::remove(root_nodes.begin(), root_nodes.end(), candidate.reference), root_nodes.end());
            }
        }

        envrn.reference = candidate.reference;
    }

    bool nodeExists(std::string name) {
        return std::count(all_nodes.begin(), all_nodes.end(), name) > 0;
    }
};


int main() {

}