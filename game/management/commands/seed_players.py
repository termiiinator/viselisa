from django.core.management.base import BaseCommand

from game.models import Player

PLAYERS = [
    {
        'name': 'buffon',
        'age': 47,
        'position': 'Goalkeeper',
        'number': 1,
        'first_club': 'Parma',
        'current_club': 'Retired',
    },
    {
        'name': 'maldini',
        'age': 56,
        'position': 'Defender',
        'number': 3,
        'first_club': 'AC Milan',
        'current_club': 'Retired',
    },
    {
        'name': 'totti',
        'age': 49,
        'position': 'Forward',
        'number': 10,
        'first_club': 'AS Roma',
        'current_club': 'Retired',
    },
    {
        'name': 'delpiero',
        'age': 51,
        'position': 'Forward',
        'number': 10,
        'first_club': 'Padova',
        'current_club': 'Retired',
    },
    {
        'name': 'pirlo',
        'age': 46,
        'position': 'Midfielder',
        'number': 21,
        'first_club': 'Brescia',
        'current_club': 'Retired',
    },
    {
        'name': 'chiellini',
        'age': 41,
        'position': 'Defender',
        'number': 3,
        'first_club': 'Livorno',
        'current_club': 'Los Angeles FC',
    },
    {
        'name': 'bonucci',
        'age': 39,
        'position': 'Defender',
        'number': 19,
        'first_club': 'Inter',
        'current_club': 'Fenerbahce',
    },
    {
        'name': 'verratti',
        'age': 33,
        'position': 'Midfielder',
        'number': 7,
        'first_club': 'Pescara',
        'current_club': 'Al Arabi',
    },
    {
        'name': 'barella',
        'age': 29,
        'position': 'Midfielder',
        'number': 23,
        'first_club': 'Cagliari',
        'current_club': 'Inter',
    },
    {
        'name': 'donnarumma',
        'age': 27,
        'position': 'Goalkeeper',
        'number': 1,
        'first_club': 'AC Milan',
        'current_club': 'Paris Saint-Germain',
    },
]


class Command(BaseCommand):
    help = 'Seed players table with Italian footballers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing players before insert.',
        )

    def handle(self, *args, **options):
        if options['reset']:
            deleted_count, _ = Player.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Removed {deleted_count} existing rows.'))

        created_count = 0
        for payload in PLAYERS:
            _, created = Player.objects.get_or_create(name=payload['name'], defaults=payload)
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Seed completed. Created: {created_count}.'))
