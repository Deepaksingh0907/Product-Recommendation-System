# Product Recommendation System

A Django web application that provides **content-based product recommendations** using TF-IDF vectorization and cosine similarity over product name, category, and description data.

## Features

- User signup, login, and logout
- Content-based recommendations using TF-IDF + cosine similarity
- Top 5 similar products for a searched catalog product
- Optional minimum/maximum price and minimum-rating filters
- Authenticated product creation
- Automatic TF-IDF index rebuild after a product is added
- SQLite for Django user accounts

## How Recommendations Work

1. Product name, category, and description are combined into text features.
2. `TfidfVectorizer` converts the product text into numerical vectors.
3. The searched product is located in the catalog.
4. Cosine similarity is calculated between that product vector and the catalog vectors.
5. The searched product itself is excluded and the top 5 most similar products are returned.
6. Price and rating filters are applied when supplied.

The application calculates similarity on demand instead of storing a full N x N similarity matrix in Git. This keeps the repository smaller and avoids committing generated model artifacts.

## Tech Stack

- **Backend:** Django 5.2
- **ML / data:** pandas, scikit-learn
- **Recommendation:** `TfidfVectorizer` + cosine similarity
- **Database:** SQLite
- **Frontend:** Django templates, Bootstrap, CSS

## Project Structure

```text
Product-Recommendation-System/
├── data/
│   └── cleaned_product_data.csv
├── product_recommender/
│   ├── settings.py
│   └── urls.py
├── recommender/
│   ├── services/
│   │   └── recommendation_service.py
│   ├── templates/
│   ├── static/
│   ├── urls.py
│   └── views.py
├── manage.py
├── prepare_data.py
├── pyproject.toml
└── README.md
```

## Getting Started

### Requirements

- Python 3.11+
- `uv` or pip

### Setup

```bash
git clone git@github.com:Deepaksingh0907/Product-Recommendation-System.git
cd Product-Recommendation-System
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

With pip, install Django, pandas, and scikit-learn, then run the standard Django migration and server commands.

## Usage

1. Create an account and log in.
2. Enter the name of a product that exists in the catalog.
3. Optionally set price/rating filters.
4. Click **Recommend Products**.
5. The application returns up to five similar products ranked by cosine similarity.

Authenticated users can also add products. The combined recommendation text is generated automatically when it is not supplied, and the TF-IDF index is rebuilt after the catalog changes.

## Dataset Preparation

`prepare_data.py` can be used with a local `amazon.csv` dataset to regenerate `data/cleaned_product_data.csv`. It may also generate local model artifacts under `saved_models/`; that directory is intentionally ignored by Git because these files are generated and can be recreated.

## Scaling Note

For this demo, cosine similarity is calculated against the in-memory catalog. For a much larger product catalog, a nearest-neighbor/vector index would be more appropriate than storing or calculating a full pairwise similarity matrix.
