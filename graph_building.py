import networkx as nx
from matplotlib import pyplot as plt
import matplotlib

# Ensure a compatible backend
matplotlib.use("TkAgg")  # Use a GUI backend (adjust based on your system)

def build_graph(entities, relations):
    graph = nx.DiGraph()

    for entity in entities:
        graph.add_node(entity[0], label=entity[1])

    for relation in relations:
        graph.add_edge(relation[2], relation[0], label=relation[1])
    
# Save the graph in GML format
    nx.write_gml(graph, 'graph.gml')

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='lightgreen', node_size=3000, font_size=10, arrowsize=20)
    edge_labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
    plt.title('Simple Network Graph')

    # Display or save the graph
    try:
        plt.show()
    except:
        plt.savefig('network_graph.png')
        print("Graph saved as 'network_graph.png'")
