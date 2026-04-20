import re

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Player
from .serializers import GuessRequestSerializer, PlayerSerializer

MAX_MISTAKES = 6
LATIN_LETTER_REGEX = re.compile(r'^[a-z]$')
HINT_ORDER = ['age', 'position', 'number', 'first_club', 'current_club']
HINT_LABELS = {
    'age': 'Возраст',
    'position': 'Позиция',
    'number': 'Игровой номер',
    'first_club': 'Первый профессиональный клуб',
    'current_club': 'Текущий клуб',
}


def home_view(request):
    return render(request, 'index.html')


def _build_masked_word(word: str, guessed_letters: list[str]) -> str:
    guessed_set = set(guessed_letters)
    return ' '.join(letter if letter in guessed_set else '_' for letter in word)


def _build_hints(state: dict) -> list[dict]:
    player = state['player']
    hints_to_show = min(state['mistakes'], len(HINT_ORDER))
    return [
        {'label': HINT_LABELS[key], 'value': str(player[key])}
        for key in HINT_ORDER[:hints_to_show]
    ]


def _build_game_response(state: dict, repeated: bool = False) -> dict:
    return {
        'masked_word': _build_masked_word(state['word'], state['guessed_letters']),
        'mistakes': state['mistakes'],
        'max_mistakes': MAX_MISTAKES,
        'guessed_letters': state['guessed_letters'],
        'wrong_letters': state['wrong_letters'],
        'hints': _build_hints(state),
        'status': state['status'],
        'repeated': repeated,
        'word': state['word'] if state['status'] != 'ongoing' else None,
    }


class RandomPlayerView(APIView):
    def get(self, request):
        player = Player.objects.order_by('?').first()
        if not player:
            return Response({'detail': 'Игроки не найдены.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(PlayerSerializer(player).data)


class NewGameView(APIView):
    def post(self, request):
        player = Player.objects.order_by('?').first()
        if not player:
            return Response({'detail': 'Игроки не найдены.'}, status=status.HTTP_404_NOT_FOUND)

        state = {
            'word': player.name.lower(),
            'player': {
                'age': player.age,
                'position': player.position,
                'number': player.number,
                'first_club': player.first_club,
                'current_club': player.current_club,
            },
            'guessed_letters': [],
            'wrong_letters': [],
            'mistakes': 0,
            'status': 'ongoing',
        }
        request.session['game_state'] = state
        return Response(_build_game_response(state))


class GuessLetterView(APIView):
    def post(self, request):
        serializer = GuessRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        game_state = request.session.get('game_state')
        if not game_state:
            return Response(
                {'detail': 'Игра не начата. Нажмите "Новая игра".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        letter = serializer.validated_data['letter'].lower().strip()
        if not LATIN_LETTER_REGEX.match(letter):
            return Response(
                {'detail': 'Введите одну букву латиницы (a-z).'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if game_state['status'] != 'ongoing':
            return Response(_build_game_response(game_state))

        if letter in game_state['guessed_letters'] or letter in game_state['wrong_letters']:
            return Response(_build_game_response(game_state, repeated=True))

        if letter in game_state['word']:
            game_state['guessed_letters'].append(letter)
        else:
            game_state['wrong_letters'].append(letter)
            game_state['mistakes'] += 1

        unique_letters = set(game_state['word'])
        if unique_letters.issubset(set(game_state['guessed_letters'])):
            game_state['status'] = 'won'
        elif game_state['mistakes'] >= MAX_MISTAKES:
            game_state['status'] = 'lost'

        request.session['game_state'] = game_state
        return Response(_build_game_response(game_state))
