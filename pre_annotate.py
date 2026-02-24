import spacy
import json

nlp = spacy.load("en_core_web_sm")

# Load your preprocessed sentences
with open("ner_preprocessed.json", "r") as f:
    sentences = json.load(f)

preannotated = []

for sent in sentences:
    text = sent["text"]
    doc = nlp(text)
    
    # Extract spaCy entities
    entities = [{"start": ent.start_char, "end": ent.end_char, "label": ent.label_} for ent in doc.ents]
    
    preannotated.append({
        "text": text,
        "entities": entities
    })

ls_json = []

for sent in preannotated:  # preannotated = spaCy predictions
    # Human annotation from original dataset
    result = []
    for ent in sent.get("entities", []):
        result.append({
            "from_name": "label",
            "to_name": "text",
            "type": "labels",
            "value": {
                "start": ent["start"],
                "end": ent["end"],
                "labels": [ent["label"]]  # original dataset label
            }
        })
    
    # ML predictions from spaCy (optional, as suggestions)
    prediction_result = []
    for ent in sent.get("spaCy_entities", []):
        prediction_result.append({
            "from_name": "label",
            "to_name": "text",
            "type": "labels",
            "value": {
                "start": ent["start"],
                "end": ent["end"],
                "labels": [ent["label"]]  # spaCy label
            }
        })
    
    # Create JSON entry for Label Studio
    ls_json.append({
        "data": {"text": sent["text"]},
        "annotations": [{"result": result}],       # original ground truth
        "predictions": [{"model_version": "spacy_en_core_web_sm",
                         "result": prediction_result}]  # spaCy suggestions
    })

# Save to JSON
import json
with open("ner_labelstudio_with_predictions.json", "w") as f:
    json.dump(ls_json, f, indent=2)