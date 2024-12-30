from wikidata.client import Client
import networkx as nx
import matplotlib.pyplot as plt

def search_entity(text):
    from SPARQLWrapper import SPARQLWrapper, JSON

    endpoint_url = "https://query.wikidata.org/sparql"
    query = f"""
    SELECT ?item ?itemLabel WHERE {{
        ?item rdfs:label "{text}"@en.
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT 1
    """
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    bindings = results.get("results", {}).get("bindings", [])
    if bindings:
        return bindings[0]["item"]["value"].split("/")[-1]  # Extract the QID
    else:
        return None

def get_visual_attributes_graph(qid):
    client = Client()
    G = nx.DiGraph()  # Directed graph to better represent hierarchy

    try:
        entity = client.get(qid, load=True)
        entity_label = entity.label.get("en", f"Entity {qid}")
        G.add_node(entity_label, type='entity')

        for prop_id, prop_values in entity.data['claims'].items():
            prop_entity = client.get(prop_id)
            prop_label = prop_entity.label.get("en", f"Property {prop_id}").lower()

            if 'color' in prop_label:  # Look specifically for "color" properties
                G.add_node(prop_label, type='property')
                G.add_edge(entity_label, prop_label)

                for val in prop_values:
                    value = val.get('mainsnak', {}).get('datavalue', {}).get('value')
                    if isinstance(value, dict) and 'id' in value:
                        linked_entity = client.get(value['id'])
                        value = linked_entity.label.get("en", "Unknown")
                    
                    if isinstance(value, str):
                        G.add_node(value, type='color_value')  # Add the color value node
                        G.add_edge(prop_label, value)  # Connect the color property to its value

        return G

    except Exception as e:
        return {"error": str(e)}

def visualize_graph(graph):
    plt.figure(figsize=(12, 12))

    node_colors = []
    for node, data in graph.nodes(data=True):
        if data.get('type') == 'entity':
            node_colors.append('lightblue')  # Entity nodes in blue
        elif data.get('type') == 'property':
            node_colors.append('lightgreen')  # Property nodes in green
        elif data.get('type') == 'color_value':
            node_colors.append('gray')  # Color value nodes in gray

    pos = nx.spring_layout(graph, seed=42)  # Consistent layout
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color=node_colors, font_size=10, font_weight='bold', edge_color='gray')

    plt.title("Entity Visual Attributes Graph")
    plt.show()

def graph_height(G):
    lengths = nx.single_source_shortest_path_length(G, list(G.nodes())[0])
    max_length = max(lengths.values())
    print(f"Height of the graph (longest path): {max_length}")
    return max_length

qid = search_entity('elephant')
if qid:
    graph = get_visual_attributes_graph(qid)
    if isinstance(graph, dict) and "error" in graph:
        print(f"Error: {graph['error']}")
    else:
        graph_height(graph)
        visualize_graph(graph)
else:
    print("Entity not found.")
