import os
import json
from transformers import AutoProcessor, LlavaForConditionalGeneration
from PIL import Image
import tensorflow_hub as hub
from bert_score import score
import spacy
import tensorflow as tf

gpus = tf.config.list_physical_devices('GPU')

if gpus:
    try:
        tf.config.set_logical_device_configuration(
            gpus[0],
            [tf.config.LogicalDeviceConfiguration(memory_limit=4096)]  # Limit to 4GB
        )
    except RuntimeError as e:
        print(e)


# Load Modelsmodel_name = "llava-hf/llava-1.5-7b-hf"
model_name = "llava-hf/llava-1.5-7b-hf"
processor = AutoProcessor.from_pretrained(model_name)
model = LlavaForConditionalGeneration.from_pretrained(model_name, torch_dtype="auto", device_map="auto")
use_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
nlp = spacy.load("en_core_web_sm")  # For entity extraction

# Paths
data_path = "data/Questions/train.json"  # Update path to VQA data
image_dir = "data/images/train/"

# Preprocess Image
def preprocess_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image = image.resize((224, 224))  # Adjust size to match LLaVA
    return image

# Generate Answer with LLaVA
def generate_answer(image_path, question):
    image = preprocess_image(image_path)
    input_text = f"Question: {question} Image: [IMAGE]"
    inputs = processor(input_text, return_tensors="pt")
    outputs = model.generate(**inputs)
    return processor.decode(outputs[0], skip_special_tokens=True)

# Extract Entities
def extract_entities(question):
    doc = nlp(question)
    return [(ent.text, ent.label_) for ent in doc.ents]

# Evaluate Answers
def evaluate_model(predictions, references):
    # Universal Sentence Encoder similarity
    use_scores = [1 - hub.losses.cosine_similarity(
        use_model([p])[0], use_model([r])[0]
    ) for p, r in zip(predictions, references)]

    # BERTScore
    P, R, F1 = score(predictions, references, lang="en", verbose=True)

    # Exact match
    exact_matches = [1 if p == r else 0 for p, r in zip(predictions, references)]

    return {
        "Exact Match": sum(exact_matches) / len(exact_matches),
        "USE Similarity": sum(use_scores) / len(use_scores),
        "BERTScore": {"Precision": P.mean().item(), "Recall": R.mean().item(), "F1": F1.mean().item()},
    }

# Main Pipeline
def main():
    # Load Dataset
    with open(data_path, "r") as f:
        dataset = json.load(f)

    predictions = []
    references = []

    for item in dataset:
        question = item["question"]
        answer = item["answer"]
        image_path = os.path.join(image_dir, item["image"])

        # Generate Answer
        generated_answer = generate_answer(image_path, question)

        predictions.append(generated_answer)
        references.append(answer)

        # Optional: Entity extraction and augmentation for future steps
        entities = extract_entities(question)
        print(f"Entities in question: {entities}")

    # Evaluate Model
    metrics = evaluate_model(predictions, references)
    print("Evaluation Metrics:", metrics)

if __name__ == "__main__":
    main()


'''
1) Transfer Learning
2) Ensemble Learning
3) Stable Diffusion + prompt-to-prompt (Synthetic data)
4) Instruct Pix-to-Pix
'''
