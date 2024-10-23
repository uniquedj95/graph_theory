
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

    # Test - find path between two aiports
    # departure = "TLV"
    # destination = "BUD"
    # print(f"Path from {departure} to {destination} is :")
    # print(f"{'-->'.join(airport.label for airport in graph.get_path(departure, destination))}")

    # Test - find all reachable airports from from a given airport
    start = "CDG"
    print(f"All reachable airports from {start} are: ")
    print(f"{'\n'.join(x for x in graph.get_all_reachable_vertices(start))}")