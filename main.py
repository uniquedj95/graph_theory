
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

    # staring airport
    starting_airport = "TLV"

    print(f"Analyzing routes from {starting_airport}")

    reachable_airports = graph.get_all_reachable_vertices(starting_airport)
    print(f"Currently reachable airports: {sorted(reachable_airports)}")

    additional_routes = graph.get_min_additional_edges(starting_airport)

    if additional_routes:
        print(f"Need {len(additional_routes)} additional routes: ")
        for start, end in additional_routes:
            print(f" {start} --> {end}")
    
    else:
        print("No additional routes needed!")