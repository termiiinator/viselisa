from django.db import models


class Player(models.Model):
    """Football player used as a hidden word in Hangman."""

    name = models.CharField(max_length=120)
    age = models.IntegerField()
    position = models.CharField(max_length=80)
    number = models.IntegerField()
    first_club = models.CharField(max_length=120)
    current_club = models.CharField(max_length=120)

    class Meta:
        db_table = 'players'

    def __str__(self) -> str:
        return self.name
