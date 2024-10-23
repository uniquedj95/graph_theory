from vertex import Vertex


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