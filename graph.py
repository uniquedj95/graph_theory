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

    def __str__(self) -> str:
        return "\n".join([str(edge) for edge in self.edges])
    
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
    
    def get_all_reachable_vertices(self, start_label: str) -> Set[str]:
        """
        Get all reachable vertices from the start vertex using DFS algorithm in a directed graph.

        args:
            start_label (str): The label of the starting vertex.

        returns:
            Set[str]: A set of labels of vertices reachable from the start vertex.
        """
        if start_label not in self.vertices:
            return set()
        
        def dfs(current: Vertex, visited: Set[Vertex], reachable: Set[str]) -> None:
            visited.add(current)
            reachable.add(current.label)
            for edge in current.outgoing_edges:
                neighbor = edge.end_vertex
                if neighbor not in visited:
                    dfs(neighbor, visited, reachable)
        
        start_vertex = self.vertices[start_label]
        visited = set()
        reachable = set()
        dfs(start_vertex, visited, reachable)
        return reachable
    
    def get_min_additional_edges(self, start_label: str) -> List[tuple[str, str]]:
        """
        Get the minimum number of additional edges to make all vertices reachable from the start vertex.

        args:
            start_label (str): The label of the starting vertex.

        returns:
            List[tuple[str, str]]: A list of tuples representing the additional edges to be added.
        """ 
        
        # Get all reachable vertices from the start vertex.
        reachable = self.get_all_reachable_vertices(start_label)
        
        # if all nodes are reachable from the start vertex, return an empty list.
        if len(reachable) == len(self.vertices): return []

        components = self.get_strogestly_connected_components()

        # create a mapping of vertex to its component
        vertex_to_component = {}
        for i, component in enumerate(components):
            for vertex in component:
                vertex_to_component[vertex] = i

        # find which component is reachable from the start vertex
        reachable_components = set()
        for vertex in reachable:
            reachable_components.add(vertex_to_component[vertex])

        # find additional edges needed
        additional_edges = []
        unreachable_vertices = set(self.vertices.keys()) - reachable

        while unreachable_vertices:
            from_vertex = min(reachable)
            to_vertex = min(unreachable_vertices)
            additional_edges.append((from_vertex, to_vertex))
            reachable = self.get_all_reachable_vertices(start_label)
            unreachable_vertices = set(self.vertices.keys()) - reachable
        
        return additional_edges
    

    def get_strogestly_connected_components(self) -> List[Set[str]]:
        """
        Get the strongly connected components of the graph using Kosaraju's algorithm.

        Returns:
            List[Set[str]]: A list of strongly connected components.
        """
        def dfs(current: Vertex, visited: Set[Vertex], stack: List[Vertex]) -> None:
            visited.add(current)
            for neighbor in current.outgoing_edges:
                if neighbor.end_vertex not in visited:
                    dfs(neighbor.end_vertex, visited, stack)
            stack.append(current)
        
        def reverse_edges() -> None:
            for edge in self.edges:
                edge.start_vertex, edge.end_vertex = edge.end_vertex, edge.start_vertex
        
        def dfs_reverse(current: Vertex, visited: Set[Vertex], component: Set[str]) -> None:
            visited.add(current)
            component.add(current.label)
            for neighbor in current.outgoing_edges:
                if neighbor.end_vertex not in visited:
                    dfs_reverse(neighbor.end_vertex, visited, component)
        
        # First DFS to fill the stack.
        visited = set()
        stack = []
        for vertex in self.vertices.values():
            if vertex not in visited:
                dfs(vertex, visited, stack)
        
        # Reverse the edges.
        reverse_edges()
        
        # Second DFS to get the strongly connected components.
        visited = set()
        components = []
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                component = set()
                dfs_reverse(vertex, visited, component)
                components.append(component)
        
        return components

