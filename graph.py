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
    
    def count_min_additional_edges(self, start_label: str) -> int:
        """
        Calculate the minimum number of additional edges needed to make all airports reachable.

        args:
            start_label (str): The label of the starting vertex.

        Returns:
            int: The minimum number of additional one-way routes.
        """
        # Find all SCCs
        sccs = self.get_strongly_connected_components()

        # Build the condensed graph
        condensed_graph = self.build_condensed_graph(sccs)

        # Find SCC of the start vertex
        start_component = -1
        for i, component in enumerate(sccs):
            if start_label in component:
                start_component = i
                break

        # Calculate in-degrees of the condensed graph nodes
        in_degrees = {i: 0 for i in range(len(sccs))}
        for node, neighbors in condensed_graph.items():
            for neighbor in neighbors:
                in_degrees[neighbor] += 1

        # Count nodes with in-degree = 0 (excluding the start SCC)
        zero_in_degree_count = 0
        for node in range(len(sccs)):
            if in_degrees[node] == 0 and node != start_component:
                zero_in_degree_count += 1

        return zero_in_degree_count

    def get_strongly_connected_components(self) -> List[Set[str]]:
        """
        Get the strongly connected components of the graph using Tarjan's algorithm.

        Returns:
            List[Set[str]]: A list of strongly connected components.
        """
        index = 0
        stack: List[Vertex] = []
        indices = {}
        lowlinks = {}
        on_stack = set()
        components = []

        def strongconnect(vertex: Vertex) -> None:
            nonlocal index
            indices[vertex] = index
            lowlinks[vertex] = index
            index += 1
            stack.append(vertex)
            on_stack.add(vertex)

            for edge in vertex.outgoing_edges:
                neighbor = edge.end_vertex
                if neighbor not in indices:
                    strongconnect(neighbor)
                    lowlinks[vertex] = min(lowlinks[vertex], lowlinks[neighbor])
                elif neighbor in on_stack:
                    lowlinks[vertex] = min(lowlinks[vertex], indices[neighbor])

            if lowlinks[vertex] == indices[vertex]:
                component = set()
                while True:
                    w = stack.pop()
                    on_stack.remove(w)
                    component.add(w.label)
                    if w == vertex:
                        break
                components.append(component)

        for vertex in self.vertices.values():
            if vertex not in indices:
                strongconnect(vertex)

        return components
    
    def build_condensed_graph(self, sccs: List[Set[str]]) -> Dict[int, Set[int]]:
        """
        Build a new graph where each SCC is treated as a single node.

        args:
            sccs (List[Set[str]]): A list of SCCs, each as a set of vertex labels.

        Returns:
            Dict[int, Set[int]]: The condensed graph where each key is an SCC, and the value is a set of connected SCCs.
        """
        component_map = {}
        for i, component in enumerate(sccs):
            for label in component:
                component_map[label] = i

        condensed_graph = {i: set() for i in range(len(sccs))}

        for edge in self.edges:
            start_component = component_map[edge.start_vertex.label]
            end_component = component_map[edge.end_vertex.label]
            if start_component != end_component:
                condensed_graph[start_component].add(end_component)

        return condensed_graph