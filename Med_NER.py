
from transformers import pipeline

# Load the pipeline for token classification (NER)
pipe = pipeline("token-classification", model="alvaroalon2/biobert_diseases_ner", grouped_entities=True)

# Sample input text
sample_text = "The patient was diagnosed with diabetes mellitus type 2 and hypertension."

# Run the pipeline
entities = pipe(sample_text)

# Display the recognized entities
print("Recognized Entities:")
for entity in entities:
    print(f"Entity: {entity['word']}, Label: {entity['entity_group']}, Score: {entity['score']:.2f}")
