from edge import Edge
from vertex import Vertex
from typing import Dict, List, Optional, Set

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
            
            for neighbor in current.get_neighbours():
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