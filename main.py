from wiki_scraping import fetch_wikipedia_page
from entity_recognition import extract_entities_relations
from graph_building import build_graph 

# print(fetch_wikipedia_page('adrenaline cancer'))

content = fetch_wikipedia_page('cancer')

print("entering entity recognition")

entities, relations = extract_entities_relations(content)

print('building graph')
build_graph(entities,relations)
