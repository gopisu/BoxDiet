from django.contrib.auth.models import User as Auth_user
from django.test import TestCase
from django.urls import reverse

from BoxDiet.models import User


class ViewsTest(TestCase):
    def setUp(self):
        test_user1 = Auth_user.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )
        test_user2 = Auth_user.objects.create_user(
            username="testuser2", password="2HJ1vRV0Z&3iD"
        )

        test_user1.save()
        test_user2.save()

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

    #
    # def test_logged_in_with_permission_borrowed_book(self):
    #     login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
    #     response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk}))
    #
    #     # Check that it lets us login - this is our book and we have the right permissions.
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_logged_in_with_permission_another_users_borrowed_book(self):
    #     login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
    #     response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
    #
    #     # Check that it lets us login. We're a librarian, so we can view any users book
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_HTTP404_for_invalid_book_if_logged_in(self):
    #     # unlikely UID to match our bookinstance!
    #     test_uid = uuid.uuid4()
    #     login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
    #     response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': test_uid}))
    #     self.assertEqual(response.status_code, 404)
    #
    # def test_uses_correct_template(self):
    #     login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
    #     response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
    #     self.assertEqual(response.status_code, 200)
    #
    #     # Check we used correct template
    #     self.assertTemplateUsed(response, 'catalog/book_renew_librarian.html')
