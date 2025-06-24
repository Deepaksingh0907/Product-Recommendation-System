from django.shortcuts import render
import pandas as pd
import pickle
import os

# Load model & data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'cleaned_product_data.csv'))
tfidf = pickle.load(open(os.path.join(BASE_DIR, 'saved_models', 'tfidf_vectorizer.pkl'), 'rb'))
similarity = pickle.load(open(os.path.join(BASE_DIR, 'saved_models', 'similarity_matrix.pkl'), 'rb'))

def home(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        if product_name not in df['product_name'].values:
            return render(request, 'home.html', {'error': 'Product not found'})
        index = df[df['product_name'] == product_name].index[0]
        distances = similarity[index]
        recommended_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommendations = df.iloc[[i[0] for i in recommended_indices]][[
            'product_name', 'product_link', 'img_link', 'actual_price', 'rating'
        ]]
        return render(request, 'home.html', {
            'product_name': product_name,
            'recommendations': recommendations.to_dict(orient='records')
        })
    return render(request, 'home.html')