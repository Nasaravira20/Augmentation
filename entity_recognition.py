import sys
import spacy

# print(sys.modules.keys())
# Load spaCy's language model
nlp = spacy.load("en_core_web_sm")

def extract_entities_relations(text):
    doc = nlp(text)
    print(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    relations = [(token.text, token.dep_, token.head.text) for token in doc if token.dep_ in ("nsubj", "dobj")]
    return entities, relations

if __name__ == '__main__':
    entities, relations = extract_entities_relations(content)
    print("Entities:", entities)
    print("Relations:", relations)
