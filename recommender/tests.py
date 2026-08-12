from unittest.mock import patch

import pandas as pd
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .services.recommendation_service import RecommendationService


class HomeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="secret123")

    def test_home_page_requires_login(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)

    def test_home_page_renders_for_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_add_product_requires_login(self):
        response = self.client.get(reverse("add_product"))
        self.assertEqual(response.status_code, 302)

    def test_empty_product_name_is_rejected(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("home"), {"product_name": "   "})
        self.assertContains(response, "Please enter a product name.")


class RecommendationServiceTests(TestCase):
    def setUp(self):
        self.sample_data = pd.DataFrame(
            [
                {
                    "product_name": "Phone Alpha",
                    "actual_price": 100,
                    "rating": 4.5,
                    "combined": "phone android camera",
                    "product_link": "https://example.com/a",
                    "img_link": "https://example.com/a.jpg",
                },
                {
                    "product_name": "Phone Beta",
                    "actual_price": 120,
                    "rating": 4.2,
                    "combined": "phone android camera battery",
                    "product_link": "https://example.com/b",
                    "img_link": "https://example.com/b.jpg",
                },
                {
                    "product_name": "Phone Gamma",
                    "actual_price": 200,
                    "rating": 3.5,
                    "combined": "phone android display",
                    "product_link": "https://example.com/c",
                    "img_link": "https://example.com/c.jpg",
                },
                {
                    "product_name": "Laptop Delta",
                    "actual_price": 900,
                    "rating": 4.8,
                    "combined": "laptop computer keyboard",
                    "product_link": "https://example.com/d",
                    "img_link": "https://example.com/d.jpg",
                },
            ]
        )

    def build_service(self):
        with patch("pandas.read_csv", return_value=self.sample_data.copy()):
            return RecommendationService()

    def test_unknown_product_returns_empty_list(self):
        service = self.build_service()
        self.assertEqual(service.recommend("Does Not Exist"), [])

    def test_searched_product_is_excluded(self):
        service = self.build_service()
        results = service.recommend("Phone Alpha")
        names = [item["product_name"] for item in results]
        self.assertNotIn("Phone Alpha", names)

    def test_recommendation_limit_is_respected(self):
        service = self.build_service()
        results = service.recommend("Phone Alpha", limit=2)
        self.assertLessEqual(len(results), 2)

    def test_min_price_filter(self):
        service = self.build_service()
        results = service.recommend("Phone Alpha", min_price="150")
        self.assertTrue(all(item["actual_price"] >= 150 for item in results))

    def test_min_rating_filter(self):
        service = self.build_service()
        results = service.recommend("Phone Alpha", min_rating="4.5")
        self.assertTrue(all(item["rating"] >= 4.5 for item in results))
