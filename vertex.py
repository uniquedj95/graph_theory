from typing import Set
from edge import Edge

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