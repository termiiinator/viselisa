from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Player


class HangmanApiTests(APITestCase):
    def setUp(self):
        self.player = Player.objects.create(
            name='totti',
            age=49,
            position='Forward',
            number=10,
            first_club='AS Roma',
            current_club='Retired',
        )
        self.new_game_url = reverse('new-game')
        self.guess_url = reverse('guess-letter')
        self.random_url = reverse('random-player')

    def test_random_player_returns_player_payload(self):
        response = self.client.get(self.random_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.player.id)
        self.assertEqual(response.data['name'], 'totti')

    def test_new_game_initial_state(self):
        response = self.client.post(self.new_game_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ongoing')
        self.assertEqual(response.data['mistakes'], 0)
        self.assertEqual(response.data['max_mistakes'], 6)
        self.assertEqual(response.data['hints'], [])
        self.assertEqual(response.data['masked_word'], '_ _ _ _ _')

    def test_wrong_guess_opens_first_hint(self):
        self.client.post(self.new_game_url)
        response = self.client.post(self.guess_url, {'letter': 'z'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mistakes'], 1)
        self.assertEqual(len(response.data['hints']), 1)
        self.assertEqual(response.data['hints'][0]['label'], 'Возраст')

    def test_repeated_guess_is_ignored(self):
        self.client.post(self.new_game_url)
        self.client.post(self.guess_url, {'letter': 'z'}, format='json')
        response = self.client.post(self.guess_url, {'letter': 'z'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mistakes'], 1)
        self.assertTrue(response.data['repeated'])

    def test_non_latin_letter_returns_error(self):
        self.client.post(self.new_game_url)
        response = self.client.post(self.guess_url, {'letter': 'я'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('латиницы', response.data['detail'])

    def test_game_can_be_won(self):
        self.client.post(self.new_game_url)
        for letter in ['t', 'o', 'i']:
            self.client.post(self.guess_url, {'letter': letter}, format='json')
        response = self.client.post(self.guess_url, {'letter': 'p'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'won')
        self.assertEqual(response.data['word'], 'totti')

    def test_game_has_extra_chance_after_fifth_hint(self):
        self.client.post(self.new_game_url)
        response = None
        for letter in ['a', 'b', 'c', 'd', 'e']:
            response = self.client.post(self.guess_url, {'letter': letter}, format='json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ongoing')
        self.assertEqual(response.data['mistakes'], 5)
        self.assertEqual(len(response.data['hints']), 5)

    def test_game_can_be_lost(self):
        self.client.post(self.new_game_url)
        response = None
        for letter in ['a', 'b', 'c', 'd', 'e', 'f']:
            response = self.client.post(self.guess_url, {'letter': letter}, format='json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'lost')
        self.assertEqual(response.data['mistakes'], 6)
        self.assertEqual(len(response.data['hints']), 5)
