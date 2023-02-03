import json

from django.test import TestCase


class UserCountriesCase(TestCase):
    token = ''

    def setUp(self):
        response = self.client.post(
            '/register/',
            {'username': 'test', 'password': 'test123', 'email': 'test@test.com'})
        self.assertEqual(response.status_code, 200)
        self.token = response.json()['token']

    def test_register_already_exist(self):
        response = self.client.post(
            '/register/',
            {'username': 'test', 'password': 'test123', 'email': 'test@test.com'})
        self.assertNotEqual(response.json()['error'], '')

    def test_add_country_no_token(self):
        response = self.client.post(
            '/add-country/',
            data=json.dumps({"countries": ["jordan", "south-africa", "italy"]}), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def _test_add_country(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Token {self.token}",
        }
        response = self.client.post(
            '/add-country/',
            data=json.dumps({"countries": ["jordan", "south-africa", "italy", "france", "spain"]}), content_type='application/json', **headers)
        self.assertNotEqual(response.json()['user_setting'], None)

    def _test_death_percentage(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Token {self.token}",
        }
        response = self.client.get(
            '/death-percentage/',
            {"country": "jordan"},  **headers)
        percentage = response.json()['result']
        self.assertGreaterEqual(percentage, 0)

        response = self.client.get(
            '/death-percentage/',
            {"country": "palestine"},  **headers)
        self.assertEqual(response.status_code, 400)

    def _test_top_countries(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Token {self.token}",
        }
        response = self.client.get(
            '/top-countries/',
            {"status": "confirmed"},
            **headers)
        result = response.json()['result']
        self.assertEqual(len(result), 3)
        self.assertGreaterEqual(result[0]['confirmed'], result[2]['confirmed'])

    def _test_user_stats(self):
        response = self.client.get(
            '/user-statistics/',
        )
        self.assertEqual(response.status_code, 401)
        headers = {
            "HTTP_AUTHORIZATION": f"Token {self.token}",
        }
        response = self.client.get(
            '/user-statistics/',
            **headers)
        result = response.json()['result']
        self.assertEqual(len(result), 5)

    def test_order(self):
        self._test_add_country()
        self._test_death_percentage()
        self._test_top_countries()
        self._test_user_stats()
