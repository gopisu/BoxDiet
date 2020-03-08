from django.contrib.auth.models import User as Auth_user
from django.test import TestCase
from django.urls import reverse

from BoxDiet.models import User


class WhateverTest(TestCase):
    def test_user_creation(self):
        w = User.objects.create(id=5, sex="w")
        self.assertTrue(isinstance(w, User))
        self.assertEqual("w", w.sex)

    def test_view_user_ok(self):
        self.client.force_login(Auth_user.objects.get_or_create(username="testuser")[0])
        url = reverse("user_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
