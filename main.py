
from graph import DirectedGraph


def create_airport_graph() -> DirectedGraph:
    """
    Create a graph representing airports and flights.
    
    Returns:
        DirectedGraph: A graph representing airports and flights.
    """
    graph = DirectedGraph()
    
    paths = [
        ("DSM", "ORD"), ("ORD", "BGI"), ("BGI", "LGA"),
        ("JFK", "LGA"), ("ICN", "JFK"), ("HND", "ICN"),
        ("HND", "JFK"), ("EWR", "HND"), ("SFO", "DSM"), 
        ("SFO", "SAN"), ("SAN", "EYW"), ("EYW", "LHR"), 
        ("LHR", "SFO"), ("TLV", "DEL"), ("DEL", "DOH"), 
        ("DEL", "CDG"), ("CDG", "BUD"), ("CDG", "SIN"),
        ("SIN", "CDG")
    ]

    for start, end in paths:
        graph.add_edge(start, end)
    
    return graph

if __name__ == "__main__":
    graph = create_airport_graph()

    print(graph)
    
