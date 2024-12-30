from wikidata.client import Client

client = Client()
entity = client.get("Q146", load=True)  # Q146 is the ID for "Cat"
print(entity.description)  # Prints: "species of mammal"

for prop in entity.properties:
    print(prop, entity['prop'], end='\n')  # Prints: "P31", "P105", etc.