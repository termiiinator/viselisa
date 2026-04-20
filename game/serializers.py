from rest_framework import serializers

from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = (
            'id',
            'name',
            'age',
            'position',
            'number',
            'first_club',
            'current_club',
        )


class GuessRequestSerializer(serializers.Serializer):
    letter = serializers.CharField(max_length=1)
