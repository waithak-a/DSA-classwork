class graph:
    def __init__(self, directed = False):
        self.directed = directed
        
        self. directed = dict()
    def __repr__(self):
        str.graph = ""
        
        for key, value in self.adj_list.items():
            str.graph += f"{key} -> {value}"
            
        return str.graph    
    def bfs(self):
        visited = set()
        
        
    def dfs(self):
        ... 
    def add_node(self):
        if node not in self.adj_list:
            self.adj_list[node] = set()
        else:
            raise ValueError("Node already exists!!")   
    def add_edge(self, source_node, destination_node, weighted = None):
        if source_node not in self.adj_list:
            self.add_node(source_node)
            
        if destination_node not in self.adj_list:
             self.add_node(destination_node) 
             
        if weighted is None:
            self.adj_list(source_node).add(destination_node)
            if self.directed:
                self.adj_list[destination_node].add(source_node)         
        else:
            self.adj_list[source_node].add((destination_node, weighted))
            
    def obtain_neighbours(self, key_node):
        return self.adj_list[key_node, set()]        
    def adj_matrix(self):
        ...
if __name__ == '__main__':
    graph_obj = graph()      
                      