# 🏷️ NER Corpus Annotation Pipeline

A complete **Named Entity Recognition (NER) data annotation pipeline** that takes a raw NER corpus, preprocesses it into sentence-level records, uses **spaCy** for automatic pre-annotation, imports into **Label Studio** for human review and correction, and exports a production-ready annotated corpus in both **JSON** and **CoNLL** formats.

---

## 📌 Project Overview

This project demonstrates an end-to-end NLP data annotation workflow — from raw CSV data all the way to a human-validated, export-ready NER corpus. It combines automated ML-assisted pre-annotation with human-in-the-loop review, significantly reducing manual labeling effort while maintaining high annotation quality.

**Entity Types Annotated:**

| Label | Description           |
|-------|-----------------------|
| `PER` | Person names          |
| `ORG` | Organizations         |
| `LOC` | Locations / Places    |
| `MISC`| Miscellaneous entities|

---

## 🗂️ Project Structure

```
NER Project/
│
├── Named Entity Recognition (NER) Corpus/
│   └── ner.csv                         # Raw source dataset (47,959 token rows, BIO-tagged)
│
├── Preprocess.ipynb                    # Step 1: Data loading & sentence-level preprocessing
├── pre_annotate.py                     # Step 2: spaCy pre-annotation + Label Studio JSON export
│
├── ner_preprocessed.json               # Intermediate: Cleaned sentence-level records
├── ner_labelstudio_preannotated.json   # Label Studio import (annotations only)
├── ner_labelstudio_with_predictions.json # Label Studio import (annotations + spaCy predictions)
│
├── final_export.json                   # Output: Final human-reviewed annotations (JSON)
├── final_export.conll                  # Output: Final annotations in CoNLL-2003 format
│
├── Before Manual Annotation.png        # Screenshot: Label Studio before human review
├── After Manual Annotation.png         # Screenshot: Label Studio after human review
│
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

---

## ⚙️ Pipeline Walkthrough

### Step 1 — Preprocess (`Preprocess.ipynb`)

Loads the raw `ner.csv` (a token-per-row BIO-tagged corpus with `Sentence #`, `Sentence`, `POS`, and `Tag` columns). Groups tokens by sentence, reconstructs full sentence strings, and converts BIO tags into character-offset entity spans compatible with Label Studio.

**Output:** `ner_preprocessed.json` — a list of sentence objects:
```json
[
  {
    "text": "Thousands of demonstrators have marched through London ...",
    "entities": [
      { "start": 47, "end": 53, "label": "geo" }
    ]
  }
]
```

---

### Step 2 — Pre-annotate (`pre_annotate.py`)

Runs **spaCy** (`en_core_web_sm`) over every sentence to produce automatic entity predictions. Structures the output as a Label Studio-compatible JSON with:
- `annotations` — ground-truth labels from the original dataset (displayed to the annotator)
- `predictions` — spaCy's suggestions (shown as pre-filled labels that the annotator can accept or correct)

**Output:** `ner_labelstudio_with_predictions.json`

---

### Step 3 — Human Annotation in Label Studio

The pre-annotated JSON is imported into **Label Studio** where a human annotator reviews each sentence, corrects any mislabelled entities, and validates the spaCy suggestions. This hybrid workflow dramatically reduces labeling time compared to labeling from scratch.

#### Before Annotation
*Entities are not yet highlighted — the annotator is about to begin labeling.*

![Before Annotation](Before%20Manual%20Annotation.png)

#### After Annotation
*Entities are highlighted and confirmed. The right panel shows the labeled regions: **LOC** Beirut, **LOC** New York, **ORG** United Nations, **PER** Fouad Siniora.*

![After Annotation](After%20Manual%20Annotation.png)

---

### Step 4 — Export

After all sentences are reviewed, Label Studio exports the final dataset in two formats:
- **`final_export.json`** — Full Label Studio JSON with all annotation metadata, usable for model training with frameworks like Hugging Face or spaCy.
- **`final_export.conll`** — Standard CoNLL-2003 format (`token -X- _ LABEL`), compatible with most NER model training pipelines.

**CoNLL sample:**
```
-DOCSTART- -X- O

Thousands -X- _ B-CARDINAL
of        -X- _ O
London    -X- _ B-GPE
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Label Studio (for annotation review)

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Download the spaCy model

```bash
python -m spacy download en_core_web_sm
```

### 3. Run the preprocessing notebook

Open `Preprocess.ipynb` in Jupyter and run all cells. This generates `ner_preprocessed.json`.

```bash
jupyter notebook Preprocess.ipynb
```

### 4. Run the pre-annotation script

```bash
python pre_annotate.py
```

This generates `ner_labelstudio_with_predictions.json`, ready for import into Label Studio.

### 5. Import into Label Studio

1. Create a new Label Studio project with the **NLP → Named Entity Recognition** template.
2. Import `ner_labelstudio_with_predictions.json` as tasks.
3. Review, correct, and submit annotations.
4. Export as **JSON** or **CoNLL 2003**.

---

## 📊 Dataset

The source data is a widely-used **NER benchmark corpus** containing news wire text, originally annotated with BIO tags across **47,959 token rows** spanning thousands of sentences.

**Source columns in `ner.csv`:**

| Column       | Description                                  |
|-------------|----------------------------------------------|
| `Sentence #` | Sentence identifier                          |
| `Sentence`   | Individual token (one word per row)          |
| `POS`        | Part-of-speech tag                           |
| `Tag`        | BIO NER tag (e.g., `B-geo`, `I-per`, `O`)   |

---

## 🧰 Technologies Used

| Tool / Library | Purpose |
|----------------|---------|
| **Python**     | Core scripting language |
| **pandas**     | CSV loading and sentence grouping |
| **spaCy**      | Automatic pre-annotation (`en_core_web_sm`) |
| **Label Studio** | Human annotation interface |
| **Jupyter**    | Interactive data exploration and preprocessing |

---

## 📄 License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).
