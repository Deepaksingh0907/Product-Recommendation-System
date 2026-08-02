from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import pandas as pd
import pickle
import os
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'cleaned_product_data.csv'))

df['actual_price'] = (
    df['actual_price']
    .astype(str)
    .str.replace(r'[^\d.]', '', regex=True)
    .str.replace(',', '')
    .astype(float)
)
def update_similarity_matrix(df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined'].fillna(''))
    similarity = cosine_similarity(tfidf_matrix)
    return tfidf, similarity
tfidf, similarity = update_similarity_matrix(df)
@login_required
def home(request):
    global df
    if request.method == 'POST':
        product_name = request.POST.get('product_name') or ''
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        min_rating = request.POST.get('min_rating')

        # Split the search string into keywords and filter products containing any keyword
        search_keywords = [kw.strip().lower() for kw in product_name.split() if kw.strip()]
        if search_keywords:
            mask = df['product_name'].str.lower().apply(
                lambda name: any(kw in name for kw in search_keywords)
            )
            products = df[mask].copy()
        else:
            products = df.copy()

        products['actual_price'] = pd.to_numeric(products['actual_price'], errors='coerce')
        products['rating'] = pd.to_numeric(products['rating'], errors='coerce')

        if min_price:
            products = products[products['actual_price'] >= float(min_price)]
        if max_price:
            products = products[products['actual_price'] <= float(max_price)]
        if min_rating:
            products = products[products['rating'] >= float(min_rating)]

        if products.empty:
            return render(request, 'home.html', {
                'error': 'No product found with the given criteria.',
                'product_name': product_name
            })

        product_list = products[['product_name', 'product_link', 'img_link', 'actual_price', 'rating']].to_dict(orient='records')

        return render(request, 'home.html', {
            'product_name': product_name,
            'product_list': product_list
        })

    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            return redirect('login')
        return render(request, 'signup.html', {'error': 'User already exists'})
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def add_product(request):
    global df, tfidf, similarity
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        category = request.POST.get('category')
        actual_price = request.POST.get('actual_price')
        rating = request.POST.get('rating')
        about_product = request.POST.get('about_product')
        img_link = request.POST.get('img_link')
        product_link = request.POST.get('product_link')
        combined = request.POST.get('combined')

        csv_path = os.path.join(BASE_DIR, 'data', 'cleaned_product_data.csv')
        df = pd.read_csv(csv_path)
        new_product = {
            'product_id': product_id,
            'product_name': product_name,
            'category': category,
            'actual_price': actual_price,
            'rating': rating,
            'about_product': about_product,
            'img_link': img_link,
            'product_link': product_link,
            'combined': combined
        }
        df = pd.concat([df, pd.DataFrame([new_product])], ignore_index=True)
        df.to_csv(csv_path, index=False)
        # Clean actual_price column again
        df['actual_price'] = (
            df['actual_price']
            .astype(str)
            .str.replace(r'[^\d.]', '', regex=True)
            .str.replace(',', '')
            .astype(float)
        )
        # Update similarity matrix and tfidf
        tfidf, similarity = update_similarity_matrix(df)
        return render(request, 'add_product.html', {'success': True})

    return render(request, 'add_product.html')

def logout_view(request):
    logout(request)
    return redirect('login')