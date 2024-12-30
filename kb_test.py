
import json
from SPARQLWrapper import SPARQLWrapper, JSON
import wikipediaapi

# Initialize SPARQL endpoint
def query_wikidata():
    """
    Query Wikidata to retrieve hierarchical entity data and basic relationships.
    """
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """
    SELECT ?entity ?entityLabel ?parent ?parentLabel WHERE {
        ?entity wdt:P31 wd:Q16521.  # Instance of "taxon" (replace with suitable type if needed)
        ?entity wdt:P279 ?parent.  # Subclass of another entity
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    } LIMIT 100
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    entities = []
    for result in results["results"]["bindings"]:
        entity = {
            "entity": result["entityLabel"]["value"],
            "parent": result["parentLabel"]["value"],
            "entity_id": result["entity"]["value"].split("/")[-1],  # Extract QID
            "parent_id": result["parent"]["value"].split("/")[-1],
        }
        entities.append(entity)
    return entities


# Wikipedia attribute extraction

import requests

def fetch_attributes_from_wikipedia(entity_name):
    """
    Fetch attributes for a given entity from Wikipedia using MediaWiki API.
    """
    # Define User-Agent as per Wikipedia policy
    headers = {
        "User-Agent": "CoolBot/1.0 (https://example.org/coolbot/; coolbot@example.org)"
    }

    # API endpoint and parameters
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": True,
        "titles": entity_name
    }

    # Make API request
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error fetching page for '{entity_name}': HTTP {response.status_code}")
        return {}

    # Parse the response JSON
    data = response.json()
    page = next(iter(data["query"]["pages"].values()))

    if 'extract' not in page:
        print(f"No content found for page: {entity_name}")
        return {}

    content = page['extract']

    # Extract attributes from content (example logic)
    attributes = {}
    if "color" in content.lower():
        attributes["color"] = ["blue", "dark blue"]  # Placeholder; improve parsing logic
    if "location" in content.lower():
        attributes["location"] = ["coral reef", "sandy beach"]
    if "pattern" in content.lower():
        attributes["pattern"] = ["spotted", "striped"]

    return attributes
def fetch_attributes_from_wikipedia(entity_name):
    """
    Fetch attributes for a given entity from Wikipedia.
    """
    user_agent = "CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org) generic-library/0.0)"  # Replace with your details
    wiki = wikipediaapi.Wikipedia("en", user_agent=user_agent)

    page = wiki.page(entity_name)

    if not page.exists():
        print(f"Page for '{entity_name}' does not exist.")
        return {}

    attributes = {}
    # Parse page text for attributes (simplified for demo purposes)
    if "color" in page.summary.lower():
        attributes["color"] = ["blue", "dark blue"]  # Placeholder; actual parsing logic needed
    if "location" in page.summary.lower():
        attributes["location"] = ["coral reef", "sandy beach"]
    if "pattern" in page.summary.lower():
        attributes["pattern"] = ["spotted", "striped"]

    return attributes



# Build the knowledge base
def build_knowledge_base():
    """
    Combine Wikidata query and Wikipedia scraping to build a structured knowledge base.
    """
    print("Querying Wikidata...")
    entities = query_wikidata()

    knowledge_base = []
    print(f"Fetched {len(entities)} entities from Wikidata.")

    for entity in entities:
        entity_name = entity["entity"]
        print(f"Fetching attributes for: {entity_name}...")
        attributes = fetch_attributes_from_wikipedia(entity_name)
        if attributes:
            knowledge_base.append({
                "entity": entity_name,
                "parent": entity["parent"],
                "entity_id": entity["entity_id"],
                "attributes": attributes,
            })

    # Save to JSON
    with open("knowledge_base.json", "w") as kb_file:
        json.dump(knowledge_base, kb_file, indent=4)
    print("Knowledge base saved as 'knowledge_base.json'.")


if __name__ == "__main__":
    build_knowledge_base()
