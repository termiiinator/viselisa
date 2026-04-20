from django.urls import path

from .views import GuessLetterView, NewGameView, RandomPlayerView

urlpatterns = [
    path('players/random/', RandomPlayerView.as_view(), name='random-player'),
    path('game/new/', NewGameView.as_view(), name='new-game'),
    path('game/guess/', GuessLetterView.as_view(), name='guess-letter'),
]
