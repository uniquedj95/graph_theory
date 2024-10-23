
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

    test_cases = ["LGA", "TLV", "HND"]

    for test_case in test_cases:
        additional_routes = graph.count_min_additional_edges(test_case)

        if additional_routes:
            print(f"Need minimum of {additional_routes} additional routes from {test_case}")
        else:
            print(f"No additional routes needed from {test_case}")