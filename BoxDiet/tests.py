from django.contrib.auth.models import User as Auth_user
from django.test import TestCase
from django.urls import reverse

from BoxDiet import factories
from BoxDiet.models import User


class ViewsTest(TestCase):
    def setUp(self):
        self.test_user1 = Auth_user.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )
        self.test_user1.save()
        self.meal_1 = factories.MealFactory()

    def test_user_creation(self):
        w = User.objects.create(id=5, sex="w")
        self.assertTrue(isinstance(w, User))
        self.assertEqual("w", w.sex)

    def test_view_user_ok(self):
        self.client.force_login(Auth_user.objects.get_or_create(username="testuser")[0])
        url = reverse("user_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.client.logout()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("dashboard"), follow=True)
        self.assertRedirects(
            response, "/box/login/?next=%2F", status_code=302, target_status_code=200
        )

    def test_redirect_if_logged_in(self):
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_meal_detail_HTTP404_invalid_meal_if_logged_in(self):
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("meal_detail", kwargs={"pk": 20}))
        self.assertEqual(response.status_code, 404)

    def test_usersview_uses_correct_template(self):
        user = self.test_user1
        self.client.force_login(user)
        response = self.client.get(
            reverse("meal_detail", kwargs={"pk": self.meal_1.meal_id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/book_renew_librarian.html")
