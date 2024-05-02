#!/bin/python3

class Link:
    def __init__(self, name:str):
        self.name = name
    
    def print(self):
        print(f"Link({self.name})")

class Chain(Link):
    def __init__(self, name:str):
        super().__init__(name)
        self.links = []
        self.position = 1.0

    def print(self):
        if len(self.links) == 0:
            super().print()
            return
        
        print(f"Chain({self.name})")
        for link in self.links:
            if link is not None:
                link.print()
        

class Locker:
    def __init__(self):
        self.chains = []

    def getChain(self, node):
        for chain in self.chains:
            if chain.name == node or chain == node:
                return chain
        if isinstance(node, str):
            link = Link(node)
            self.chains.append(link)
            return link

    def createChain(self, name:str, *links):
        chain = Chain(name)
        for link in links:
            chain.links.append(self.getChain(link))
        self.chains.append(chain)
        return chain
    
    def print(self):
        for chain in self.chains:
            chain.print()
            if isinstance(chain, Chain):
                print()

if __name__ == "__main__":
    locker = Locker()
    hash1 = locker.createChain("ABF54D")
    hash = locker.createChain("sha256/ABF54D", hash1, "sha256", "hash")
    size = locker.createChain("size/32", "size", "32")
    file = locker.createChain("file/jar", "file", "jar")
    locker.createChain("Some cool file", hash, file, size)
    locker.print()
