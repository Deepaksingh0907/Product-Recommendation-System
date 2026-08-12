from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .services.recommendation_service import recommendation_service


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

    def test_blank_product_name_is_rejected(self):
        self.client.force_login(self.user)
        with patch.object(recommendation_service, "recommend") as recommend:
            response = self.client.post(reverse("home"), {"product_name": "   "})
        self.assertContains(response, "Please enter a product name.")
        recommend.assert_not_called()


class RecommendationServiceTests(TestCase):
    def test_unknown_product_returns_empty_list(self):
        result = recommendation_service.recommend("product-that-does-not-exist-xyz")
        self.assertEqual(result, [])

    def test_recommendations_are_limited_to_five(self):
        product_name = recommendation_service.df.iloc[0]["product_name"]
        result = recommendation_service.recommend(product_name)
        self.assertLessEqual(len(result), 5)

    def test_original_product_is_excluded(self):
        product_name = recommendation_service.df.iloc[0]["product_name"]
        result = recommendation_service.recommend(product_name)
        recommended_names = [item["product_name"] for item in result]
        self.assertNotIn(product_name, recommended_names)

    def test_minimum_rating_filter(self):
        product_name = recommendation_service.df.iloc[0]["product_name"]
        result = recommendation_service.recommend(product_name, min_rating="4")
        self.assertTrue(all(float(item["rating"]) >= 4 for item in result))

    def test_maximum_price_filter(self):
        product_name = recommendation_service.df.iloc[0]["product_name"]
        result = recommendation_service.recommend(product_name, max_price="1000")
        self.assertTrue(all(float(item["actual_price"]) <= 1000 for item in result))
