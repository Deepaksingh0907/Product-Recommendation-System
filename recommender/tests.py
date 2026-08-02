from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='secret123')

    def test_home_page_requires_login(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_home_page_renders_for_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
