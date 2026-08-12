import os

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_PATH = os.path.join(BASE_DIR, "data", "cleaned_product_data.csv")


class RecommendationService:
    def __init__(self):
        self.df = pd.DataFrame()
        self.tfidf = None
        self.tfidf_matrix = None
        self.reload()

    def reload(self):
        self.df = pd.read_csv(CSV_PATH)
        self.df["actual_price"] = pd.to_numeric(
            self.df["actual_price"].astype(str).str.replace(r"[^\d.]", "", regex=True),
            errors="coerce",
        )
        self.df["rating"] = pd.to_numeric(self.df["rating"], errors="coerce")

        self.tfidf = TfidfVectorizer(stop_words="english", max_features=5000)
        self.tfidf_matrix = self.tfidf.fit_transform(self.df["combined"].fillna(""))

    def recommend(self, product_name, min_price=None, max_price=None, min_rating=None, limit=5):
        matches = self.df[
            self.df["product_name"].str.contains(product_name, case=False, na=False, regex=False)
        ]
        if matches.empty:
            return []

        product_index = matches.index[0]
        scores = cosine_similarity(
            self.tfidf_matrix[product_index], self.tfidf_matrix
        ).flatten()

        ranked_indices = scores.argsort()[::-1]
        ranked_indices = [i for i in ranked_indices if i != product_index]
        products = self.df.iloc[ranked_indices].copy()

        if min_price:
            products = products[products["actual_price"] >= float(min_price)]
        if max_price:
            products = products[products["actual_price"] <= float(max_price)]
        if min_rating:
            products = products[products["rating"] >= float(min_rating)]

        columns = ["product_name", "product_link", "img_link", "actual_price", "rating"]
        return products.head(limit)[columns].to_dict(orient="records")

    def add_product(self, product):
        self.df = pd.concat([self.df, pd.DataFrame([product])], ignore_index=True)
        self.df.to_csv(CSV_PATH, index=False)
        self.reload()


recommendation_service = RecommendationService()
