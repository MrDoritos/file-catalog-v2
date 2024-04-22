#!/bin/python3

class Tag:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Tag({self.name})"


class Relationship:
    def __init__(self, parent, child, strength = 1.0):
        self.parent = parent
        self.child = child
        self.strength = strength

    def __repr__(self):
        return f"Rel({self.parent.name} -> {self.child.name} : {self.strength})"


class Database:
    def __init__(self):
        self.relationships = []
        self.tags = []

    def tag_exists(self, tag):
        for existing_tag in self.tags:
            if existing_tag.name == tag.name:
                return True
        return False

    def get_tag(self, tag):
        for existing_tag in self.tags:
            if existing_tag.name == tag.name:
                return existing_tag
        return None

    def add_tag(self, tag):
        if not self.tag_exists(tag):
            self.tags.append(tag)

    def relationship_exists(self, parent_tag, child_tag):
        return self.relationship_exists(Relationship(parent_tag, child_tag, 1.0))

    def relationship_exists(self, relationship):
        for existing_relationship in self.relationships:
            if existing_relationship.parent == relationship.parent and existing_relationship.child == relationship.child:
                return True
        return False

    def get_relationship(self, parent_tag, child_tag):
        return self.get_relationship(Relationship(parent_tag, child_tag, 1.0))
    
    def get_relationship(self, relationship:Relationship):
        for existing_relationship in self.relationships:
            if existing_relationship.parent == relationship.parent and existing_relationship.child == relationship.child:
                return existing_relationship
        return None

    def add_relationship0(self, relationship:Relationship):
        self.add_relationship(relationship.parent, relationship.child, relationship.strength)

    def add_relationship(self, parent_tag, child_tag, strength=1.0):
        self.add_tag(parent_tag)
        self.add_tag(child_tag)

        relationship = Relationship(parent_tag, child_tag, strength)
        
        #add
        if not self.relationship_exists(relationship):
            self.relationships.append(relationship)
        else: #update
            existing_relationship = self.get_relationship(relationship)
            existing_relationship.strength = strength

    def get_children(self, parent_tag):
        children = []
        for relationship in self.relationships:
            if relationship.parent.name == parent_tag.name:
                children.append(relationship.child)
        return children

    def get_parents(self, child_tag):
        parents = []
        for relationship in self.relationships:
            if relationship.child.name == child_tag.name:
                parents.append(relationship.parent)
        return parents

    def get_roots(self):
        roots = []
        for tag in self.tags:
            if len(self.get_parents(tag)) < 1: #no parents
                roots.append(tag)
        return roots
    
    def get_leafs(self):
        leafs = []
        for tag in self.tags:
            if len(self.get_children(tag)) < 1: #no children
                leafs.append(tag)
        return leafs

    def compute_tree(self, tag):
        if len(self.get_parents(tag) < 1):
            return 1.0 # UNIQUE, root
        if len(self.get_children(tag) < 1):
            return 0.0 # UNIVERSAL, leaf
        
        # if not root or leaf, compute its position
        parent_vals = [self.compute_tree(parent) for parent in self.get_parents(tag)]

        average_parent_val = sum(parent_vals) / len(parent_vals)
        
        #not taking into account strength
        return average_parent_val
    
    def print_database(self):
        print("Tags:")
        for tag in self.tags:
            print(tag)
        print("Relationships:")
        for relationship in self.relationships:
            print(relationship)

    def print_tree(self, tag, depth=0, last = False):
        if depth == 0:
            print(tag) #root
        else:
            token = "|"
            if last:
                token = "\\"
            print((" " * depth) + token + "-", tag) #child

        children = self.get_children(tag)
        
        for i in range(len(children)):
            if i == len(children) - 1:
                self.print_tree(children[i], depth + 1, True)
            else:
                self.print_tree(children[i], depth + 1, False)        

def mrel(parent:Tag, child:Tag, strength = 1.0):
    return Relationship(parent, child, strength)

def mrels(parent, child, strength = 1.0):
    return Relationship(Tag(parent), Tag(child), strength)

# Example usage:
if __name__ == "__main__":
    # Create tags
    concept1 = Tag("Concept")
    hash0 = Tag("Hash")
    hash1 = Tag("13FA")
    file1 = Tag("File")
    path1 = Tag("/path/")
    linux0 = Tag("Linux Path")
    date0 = Tag("Date")
    path0 = Tag("Path")
    date1 = Tag("1/1/1999")
    date2 = Tag("1/2/1999")

    rels = [mrel(concept1, file1),
            mrel(concept1, path1),
            mrel(date1, date0),
            mrel(date2, date0),
            mrel(path1, path0),
            mrels("Concept", "Star"),
            mrel(hash1, hash0),
            mrel(linux0, path0),
            mrel(path1, linux0)]

    # Create relationships
    database = Database()

    for rel in rels:
        database.add_relationship0(rel)

    database.print_database()
    database.print_tree(concept1)
