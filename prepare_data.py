import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

# Load the dataset
df = pd.read_csv("amazon.csv")

# Keep only necessary columns
df = df[['product_id', 'product_name', 'category', 'actual_price', 'rating',
         'about_product', 'img_link', 'product_link']]

# Drop rows with missing important data
df.dropna(subset=['product_name', 'category', 'about_product'], inplace=True)

# Create combined field
df['combined'] = (
    df['product_name'].fillna('') + ' ' +
    df['category'].fillna('') + ' ' +
    df['about_product'].fillna('')
)

# Vectorize
tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
tfidf_matrix = tfidf.fit_transform(df['combined'])

# Compute similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Save cleaned data and models
os.makedirs('data', exist_ok=True)
os.makedirs('saved_models', exist_ok=True)

df.to_csv("data/cleaned_product_data.csv", index=False)

with open("saved_models/tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(tfidf, f)

with open("saved_models/similarity_matrix.pkl", "wb") as f:
    pickle.dump(cosine_sim, f)
