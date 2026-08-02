# Product Recommendation System

A Django-based web application that recommends products using **TF-IDF vectorization** and **cosine similarity** on product metadata (name, category, and description). Built on top of a cleaned Amazon product dataset, it supports user authentication, keyword-based product search with price/rating filters, and lets users add new products to the catalog.

## Features

- 🔐 **User authentication** — signup, login, and logout
- 🔍 **Product search** — search by keyword with optional filters for minimum price, maximum price, and minimum rating
- 🤖 **Content-based recommendations** — TF-IDF + cosine similarity over combined product text (name, category, description)
- ➕ **Add products** — add new products to the catalog; the similarity matrix is automatically recomputed
- 🗄️ **SQLite** database for user accounts (via Django's built-in auth system)

## Tech Stack

- **Backend:** Django 5.2
- **Data processing / ML:** pandas, scikit-learn (`TfidfVectorizer`, `cosine_similarity`)
- **Database:** SQLite
- **Frontend:** Django templates + CSS

## Project Structure

```
Product-Recommendation-System/
├── manage.py                     # Django management script
├── prepare_data.py               # One-off script to clean raw data and precompute TF-IDF/similarity
├── pyproject.toml                # Project dependencies
├── data/
│   └── cleaned_product_data.csv  # Cleaned product dataset used by the app
├── saved_models/
│   ├── tfidf_vectorizer.pkl      # Precomputed TF-IDF vectorizer
│   └── similarity_matrix.pkl     # Precomputed cosine similarity matrix
├── product_recommender/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── recommender/                  # Main Django app
    ├── views.py                  # Core logic: auth, search, recommendations
    ├── urls.py
    ├── models.py
    ├── static/                   # CSS and images
    └── templates/                # HTML templates (home, login, signup, add product)
```

## Getting Started

### Prerequisites

- Python 3.11+
- pip (or [uv](https://github.com/astral-sh/uv), since this project ships a `uv.lock` file)

### Installation

1. **Clone the repository**
   ```bash
   git clone git@github.com:Deepaksingh0907/Product-Recommendation-System.git
   cd Product-Recommendation-System
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   Using pip:
   ```bash
   pip install django pandas scikit-learn
   ```

   Or using uv (recommended, since `uv.lock` is included):
   ```bash
   uv sync
   ```

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Usage

1. **Sign up** for a new account, then **log in**.
2. On the **home page**, search for products by keyword, and optionally filter by minimum price, maximum price, and minimum rating.
3. Use the **Add Product** page to add new products to the catalog — the TF-IDF vectorizer and similarity matrix update automatically.

## Regenerating the Dataset / Models

If you want to rebuild the cleaned dataset and similarity models from a raw `amazon.csv` file:

```bash
python prepare_data.py
```

This will regenerate `data/cleaned_product_data.csv`, `saved_models/tfidf_vectorizer.pkl`, and `saved_models/similarity_matrix.pkl`.

## License

This project is currently unlicensed. Add a license of your choice if you plan to share or distribute this code.
