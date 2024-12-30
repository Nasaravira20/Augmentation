
import networkx as nx

# Load the graph from the GML file
graph = nx.read_gml('graph.gml')

# Extracting nodes and edges with their attributes
nodes = graph.nodes(data=True)  # Returns a list of nodes with their attributes
edges = graph.edges(data=True)  # Returns a list of edges with their attributes

# Extract entities (nodes) and relations (edges)
# Use .get() to safely access the 'label' attribute or assign a default value if not found
entities = [(node, data.get('label', 'Unknown entity')) for node, data in nodes]
relations = [(u, v, data.get('label', 'Unknown relation')) for u, v, data in edges]

# Function to generate text
def generate_text_from_graph(entities, relations):
    texts = []

    # Generate text based on entities
    for entity, label in entities:
        texts.append(f"A {label} was present in the scene, specifically the {entity}.")
    
    # Generate text based on relations (edges)
    for u, v, label in relations:
        texts.append(f"The {u} and {v} are related through {label}.")
    
    return texts

# Generate the texts
texts = generate_text_from_graph(entities, relations)

# Print the generated texts
for text in texts:
    print(text)
