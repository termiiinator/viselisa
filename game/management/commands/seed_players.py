from django.core.management.base import BaseCommand

from game.models import Player

PLAYERS = [
    # --- Legends (retired) ---
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
        'current_club': 'Retired',
    },
    {
        'name': 'bonucci',
        'age': 37,
        'position': 'Defender',
        'number': 19,
        'first_club': 'Inter',
        'current_club': 'Retired',
    },
    {
        'name': 'verratti',
        'age': 33,
        'position': 'Midfielder',
        'number': 6,
        'first_club': 'Pescara',
        'current_club': 'Al Arabi',
    },
    {
        'name': 'nesta',
        'age': 49,
        'position': 'Defender',
        'number': 5,
        'first_club': 'Lazio',
        'current_club': 'Retired',
    },
    {
        'name': 'cannavaro',
        'age': 52,
        'position': 'Defender',
        'number': 5,
        'first_club': 'Napoli',
        'current_club': 'Retired',
    },
    {
        'name': 'inzaghi',
        'age': 51,
        'position': 'Forward',
        'number': 9,
        'first_club': 'Piacenza',
        'current_club': 'Retired',
    },
    {
        'name': 'gattuso',
        'age': 47,
        'position': 'Midfielder',
        'number': 8,
        'first_club': 'Perugia',
        'current_club': 'Retired',
    },
    # --- Currently active ---
    {
        'name': 'donnarumma',
        'age': 26,
        'position': 'Goalkeeper',
        'number': 1,
        'first_club': 'AC Milan',
        'current_club': 'Paris Saint-Germain',
    },
    {
        'name': 'meret',
        'age': 27,
        'position': 'Goalkeeper',
        'number': 1,
        'first_club': 'Udinese',
        'current_club': 'Napoli',
    },
    {
        'name': 'vicario',
        'age': 28,
        'position': 'Goalkeeper',
        'number': 13,
        'first_club': 'Venezia',
        'current_club': 'Tottenham Hotspur',
    },
    {
        'name': 'dilorenzo',
        'age': 31,
        'position': 'Defender',
        'number': 22,
        'first_club': 'Empoli',
        'current_club': 'Napoli',
    },
    {
        'name': 'bastoni',
        'age': 25,
        'position': 'Defender',
        'number': 95,
        'first_club': 'Atalanta',
        'current_club': 'Inter',
    },
    {
        'name': 'calafiori',
        'age': 22,
        'position': 'Defender',
        'number': 33,
        'first_club': 'AS Roma',
        'current_club': 'Arsenal',
    },
    {
        'name': 'cambiaso',
        'age': 24,
        'position': 'Defender',
        'number': 27,
        'first_club': 'Genoa',
        'current_club': 'Juventus',
    },
    {
        'name': 'dimarco',
        'age': 27,
        'position': 'Defender',
        'number': 32,
        'first_club': 'Inter',
        'current_club': 'Inter',
    },
    {
        'name': 'scalvini',
        'age': 21,
        'position': 'Defender',
        'number': 42,
        'first_club': 'Atalanta',
        'current_club': 'Atalanta',
    },
    {
        'name': 'barella',
        'age': 27,
        'position': 'Midfielder',
        'number': 23,
        'first_club': 'Cagliari',
        'current_club': 'Inter',
    },
    {
        'name': 'tonali',
        'age': 24,
        'position': 'Midfielder',
        'number': 8,
        'first_club': 'Brescia',
        'current_club': 'Newcastle United',
    },
    {
        'name': 'locatelli',
        'age': 27,
        'position': 'Midfielder',
        'number': 5,
        'first_club': 'AC Milan',
        'current_club': 'Juventus',
    },
    {
        'name': 'frattesi',
        'age': 25,
        'position': 'Midfielder',
        'number': 16,
        'first_club': 'Sassuolo',
        'current_club': 'Inter',
    },
    {
        'name': 'pellegrini',
        'age': 28,
        'position': 'Midfielder',
        'number': 7,
        'first_club': 'AS Roma',
        'current_club': 'AS Roma',
    },
    {
        'name': 'ricci',
        'age': 23,
        'position': 'Midfielder',
        'number': 28,
        'first_club': 'Empoli',
        'current_club': 'Torino',
    },
    {
        'name': 'chiesa',
        'age': 27,
        'position': 'Forward',
        'number': 14,
        'first_club': 'Fiorentina',
        'current_club': 'Liverpool',
    },
    {
        'name': 'raspadori',
        'age': 24,
        'position': 'Forward',
        'number': 81,
        'first_club': 'Sassuolo',
        'current_club': 'Napoli',
    },
    {
        'name': 'scamacca',
        'age': 25,
        'position': 'Forward',
        'number': 90,
        'first_club': 'Sassuolo',
        'current_club': 'Atalanta',
    },
    {
        'name': 'retegui',
        'age': 25,
        'position': 'Forward',
        'number': 32,
        'first_club': 'Estudiantes',
        'current_club': 'Atalanta',
    },
    {
        'name': 'kean',
        'age': 24,
        'position': 'Forward',
        'number': 18,
        'first_club': 'Juventus',
        'current_club': 'Juventus',
    },
    {
        'name': 'zaccagni',
        'age': 29,
        'position': 'Forward',
        'number': 10,
        'first_club': 'Hellas Verona',
        'current_club': 'Lazio',
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
