
from SPARQLWrapper import SPARQLWrapper, JSON

# Set up the SPARQL endpoint
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# Example query for hierarchical entities
query = """
SELECT ?entity ?entityLabel ?parentLabel WHERE {
    ?entity wdt:P31 wd:Q16521. # Instance of taxon (example: species)
    ?entity wdt:P279 ?parent. # Subclass of another entity
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
} LIMIT 100
"""
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

print(results)

for result in results["results"]["bindings"]:
    print(f"Entity: {result['entityLabel']['value']}, Parent: {result['parentLabel']['value']}")
