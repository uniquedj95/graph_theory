from typing import Dict, List, Set

class Edge: 
    """
    Represents an edge in a graph.
    
    Attributes:
        start_vertex (Vertex): The starting vertex of the edge.
        end_vertex (Vertex): The ending vertex of the edge.
        weight (int): The weight of the edge.
    """
    
    def __init__(self, start_vertex: 'Vertex', end_vertex: 'Vertex', weight: int = 1):
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        self.weight = weight
        start_vertex.add_outgoing_edge(self)
        end_vertex.add_incoming_edge(self)
    
    def __str__(self) -> str:
        return f"{self.start_vertex} -> {self.end_vertex}"
    
    def __repr__(self) -> str:
        return self.__str__()


class Vertex:
    """
    Represents a vertex (Node) in a graph
    
    Attributes:
        label (str): The label of the vertex.
        incoming_edges (Set['Edge']): A set of edges directed towards this vertex.
        outgoing_edges (Set['Edge']): A set of edges directed away from this vertex.
    """
    
    def __init__(self, label: str):
        self.label = label
        self.incoming_edges: Set['Edge'] = set()
        self.outgoing_edges: Set['Edge'] = set()

    def __str__(self) -> str:
        return f"{self.label}"
    
    def __repr__(self) -> str:
        return self.__str__()

    def add_incoming_edge(self, edge: 'Edge') -> None:
        """
        Adds an incoming edge to the vertex.
        Args:
            edge (Edge): The edge to be added.
        """
        self.incoming_edges.add(edge)

    def add_outgoing_edge(self, edge: 'Edge') -> None:
        """
        Adds an outgoing edge to the vertex.
        Args:
            edge (Edge): The edge to be added.
        """
        self.outgoing_edges.add(edge)

    def get_neighbours(self) -> Set['Vertex']:
        """
        Get the set of neighboring vertices.
        Returns:
            Set[Vertex]: A set of vertices that are connected to this vertex by an edge.
        """
        return { edge.end_vertex for edge in self.outgoing_edges} | {edge.start_vertex for edge in self.incoming_edges}

    def get_in_degree(self) -> int:
        """
        Get the in-degree of the vertex.
        Returns:
            int: The number of incoming edges.
        """
        return len(self.incoming_edges)
    
    def get_out_degree(self) -> int:
        """
        Returns the out-degree of the vertex.
        Returns:
            int: The number of outgoing edges.
        """
        return len(self.outgoing_edges)

class DirectedGraph:
    """
    Represents a directed graph.
    
    Attributes:
        vertices (Dict[str, Vertex]): A list of vertices in the graph.
        edges (Set[Edge]): A list of edges in the graph.
    """
    def __init__(self):
        self.vertices: Dict[str, Vertex] = {}
        self.edges: Set[Edge] = set()
    
    def add_vertex(self, label: str) -> None:
        """
        Add a vertex if it doesn't exists.

        Args:
            label (str): The label of the vertex.
        """
        if label not in self.vertices:
            self.vertices[label] = Vertex(label)
    

    def get_vertex(self, label: str) -> Vertex:
        """
        Get a Vertex by its label. If the vertex does not exist, create it.

        args:
            label (str): The label of the vertex to get.
        
        returns:
            Vertex: The vertex with the given label.
        """
        if label not in self.vertices:
            self.add_vertex(label)

        return self.vertices[label]
    
    def add_edge(self, start: str, end: str) -> None:
        """
        Add a directed edge from start to end.

        args:
            start_label (str): The label of the starting vertex of the edge.
            end_label (str): The label of the ending vertex of the edge.
        """
        start_vertex = self.get_vertex(start)
        end_vertex = self.get_vertex(end)
        self.edges.add(Edge(start_vertex, end_vertex))
    
    def get_path(self, start_label: str, end_label: str) -> List[Vertex]:
        """
        Get a path from start to end using Depth First Search.
        
        Args:
            start_label (str): The label of the starting vertex.
            end_label (str): The label of the ending vertex.
        
        Returns:
            List[Vertex]: A list of vertices representing the path from start to end.
        """
        if start_label not in self.vertices or end_label not in self.vertices:
            return []
        
        def dfs(current: Vertex, end: Vertex, visited: Set[Vertex], path: List[Vertex]) -> bool:
            # Base case - Return if the current vertex is the end vertex.
            if current == end: return True
                
            visited.add(current)
            path.append(current)
            
            for neighbor in current.outgoing_edges:
                if neighbor not in visited:
                    if dfs(neighbor, end, visited, path):
                        return True
            
            path.pop()
            return False
        
        path: List[Vertex] = []
        dfs(self.vertices[start_label], self.vertices[end_label], set(), path)
        if path:
            path.append(self.vertices[end_label])
        return path
    
    def __str__(self) -> str:
        return "\n".join([str(edge) for edge in self.edges])