from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import CustomUser, UserFollower

class AuthAndUserAPITests(APITestCase):
    """
    Tests for API authentication (registration, login) and user profile management.
    """
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }
        self.user = CustomUser.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='password'
        )

    def test_user_registration(self):
        """Ensure a new user can be registered via the API."""
        url = reverse('rest_register')
        response = self.client.post(url, self.user_data, format='json')
        # Add a custom message to the assertion to print the response data on failure
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED,
            f"Registration failed with status {response.status_code}. Response: {response.data}"
        )
        self.assertTrue(CustomUser.objects.filter(email=self.user_data['email']).exists())

    def test_user_login_and_retrieve_details(self):
        """Ensure a user can log in and retrieve their details."""
        # Login
        login_url = reverse('rest_login')
        login_data = {'email': self.user.email, 'password': 'password'}
        response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        
        # Authenticate client with token
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Retrieve user details
        user_details_url = reverse('rest_user_details')
        response = self.client.get(user_details_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_update_user_profile(self):
        """Ensure an authenticated user can partially update their own profile (bio)."""
        self.client.force_authenticate(user=self.user)
        url = reverse('rest_user_details')
        updated_data = {'bio': 'This is my new bio.'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, 'This is my new bio.')

    def test_login_with_wrong_password(self):
        """Ensure login fails with an incorrect password."""
        login_url = reverse('rest_login')
        login_data = {'email': self.user.email, 'password': 'wrongpassword'}
        response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access', response.data)

    def test_registration_with_mismatched_passwords(self):
        """Ensure registration fails if passwords do not match."""
        url = reverse('rest_register')
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'passwordsdontmatch'
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # The error is a non-field error, so we check the content of the list
        self.assertIn("The two password fields didn't match.", str(response.data['non_field_errors']))

    def test_registration_with_existing_email(self):
        """Ensure registration fails if the email is already in use."""
        url = reverse('rest_register')
        invalid_data = self.user_data.copy()
        invalid_data['email'] = self.user.email  # Use email of existing user
        invalid_data['username'] = 'newusername'
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_registration_with_existing_username(self):
        """Ensure registration fails if the username is already in use."""
        url = reverse('rest_register')
        invalid_data = self.user_data.copy()
        invalid_data['username'] = self.user.username # Use username of existing user
        invalid_data['email'] = 'newemail@example.com'
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)


class UserViewSetTests(APITestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(email='user1@example.com', username='user1', password='password123')
        self.user2 = CustomUser.objects.create_user(email='user2@example.com', username='user2', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_list_users(self):
        """Ensure we can list users."""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_user_profile(self):
        """Ensure we can retrieve a single user's profile by username."""
        url = reverse('user-detail', kwargs={'username': self.user2.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user2.username)

    def test_follow_user(self):
        """Ensure a user can follow another user."""
        url = reverse('user-follow-unfollow', kwargs={'username': self.user2.username})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(UserFollower.objects.filter(user=self.user2, follower=self.user1).exists())

    def test_unfollow_user(self):
        """Ensure a user can unfollow another user."""
        UserFollower.objects.create(user=self.user2, follower=self.user1)
        url = reverse('user-follow-unfollow', kwargs={'username': self.user2.username})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(UserFollower.objects.filter(user=self.user2, follower=self.user1).exists())

    def test_follow_self(self):
        """Ensure a user cannot follow themselves."""
        url = reverse('user-follow-unfollow', kwargs={'username': self.user1.username})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_follow_already_following(self):
        """Ensure following an already followed user returns a success message without creating a duplicate."""
        UserFollower.objects.create(user=self.user2, follower=self.user1)
        url = reverse('user-follow-unfollow', kwargs={'username': self.user2.username})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserFollower.objects.filter(user=self.user2, follower=self.user1).count(), 1)

    def test_unauthenticated_user_cannot_follow(self):
        """Ensure an unauthenticated user receives a 401 Unauthorized error."""
        # Create a new client without authentication
        unauthenticated_client = APIClient()
        url = reverse('user-follow-unfollow', kwargs={'username': self.user2.username})
        response = unauthenticated_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
