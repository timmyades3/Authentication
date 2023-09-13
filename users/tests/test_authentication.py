from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestViews(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_home_view(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_register_view(self):
        response = self.client.get(self.register_url)
        # Redirects to home when logged in
        self.assertEqual(response.status_code, 302)

        self.client.logout()
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login_view(self):
        response = self.client.get(self.login_url)
        # Redirects to home when logged in
        self.assertEqual(response.status_code, 302)

        self.client.logout()
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout_view(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logout.html')

    def test_register_post(self):
        self.client.logout()
        data = {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_authenticated_user_redirected_to_home(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.home_url)

    def test_try_register_when_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.register_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'home.html')  
        self.assertRedirects(response,self.home_url)

    def test_try_home_when_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 302)
        self.login_url = '/login/?login=/'
        self.assertRedirects(response,self.login_url)

    def test_register_with_mismatched_passwords(self):
        self.client.logout()
        data = {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'mismatchedpassword' 
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertContains(response, 'The two password fields didn’t match.')
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_register_with_already_existing_username(self):
        self.client.logout()
        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword' 
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertContains(response, 'A user with that username already exists.')
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_post(self):
        self.client.logout()
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == self.home_url)

    def test_login_with_invalid_password(self):
        self.client.logout()
        data = {
            'username': 'testuser',
            'password': 'testpassword1'
        }
        response = self.client.post(self.login_url, data)
        # Expect a response with status code 200 (unsuccessful login)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        # Expect an error message in the response
        self.assertContains(response, 'Incorrect password')
        self.assertFalse(response.context['user'].is_authenticated)
   
    def test_login_non_existing_user(self):
        self.client.logout()
        data = {
            'username': 'testuser1',
            'password': 'testpassword1'
        }
        response = self.client.post(self.login_url, data)
        # Expect a response with status code 200 (unsuccessful login)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        # Expect an error message in the response
        self.assertContains(response, 'User does not exist.')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout_get(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logout.html')


class SessionFixationTest(TestCase):
    def test_session_id_change_on_login(self):
        self.client.login(username='testuser', password='testpassword')
        session_id_before = self.client.session.session_key

        # Log out to end the session
        self.client.logout()

        # Log in again as the same user and get the new session ID
        self.client.login(username='testuser', password='testpassword')
        session_id_after = self.client.session.session_key

        # Ensure that the session ID changes after login
        self.assertNotEqual(session_id_before, session_id_after)

class CSRFAttackTest(TestCase):
    def test_csrf_attack_attempt(self):
        # Try to make a POST request to the registration view
        response = self.client.post(reverse('register'), data={'data': 'malicious_data'})

        # Ensure that the request is denied (status code 403)
        self.assertEqual(response.status_code, 403)

# class CSRFAttackTest(TestCase):
#     def test_csrf_attack_attempt(self):

#         self.client.login(username='testuser', password='testpassword')

#         # Try to make a POST request to a view that requires CSRF protection
#         response = self.client.post(reverse('login'), data={'data': 'malicious_data'})

#         # Ensure that the request is denied (status code 403)
#         self.assertEqual(response.status_code, 403)        