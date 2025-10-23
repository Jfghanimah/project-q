import json
from datetime import datetime
from django.core.management.base import BaseCommand
from games.models import Game, Publisher, Studio, Platform, Genre

class Command(BaseCommand):
    help = 'Import games from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file containing game data')

    def handle(self, *args, **options):
        json_file = options['json_file']

        try:
            with open(json_file, 'r') as f:
                games_data = json.load(f)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error reading JSON file: {e}"))
            return

        # Assuming the JSON file contains a list of game dictionaries
        for entry in games_data:
            title = entry.get('title')
            release_date = entry.get('release_date')
            publisher_name = entry.get('publisher')
            developer_name = entry.get('developer')
            platforms_list = entry.get('platforms', [])
            genres_list = entry.get('genre', [])
            age_rating = entry.get('age_rating', '')
            # Create or get the Publisher (you can fill in description as needed)
            publisher, _ = Publisher.objects.get_or_create(name=publisher_name, defaults={'description': ''})
            # Create or get the Studio from the 'developer' field
            studio, _ = Studio.objects.get_or_create(name=developer_name, defaults={'description': ''})
            
            # Create the Game object; using empty string for description and None for box_art as placeholders
            game, created = Game.objects.get_or_create(
                title=title,
                release_date=release_date,
                defaults={'description': f"Age Rating: {age_rating}", 'box_art': "box_art/default_boxart.jpg"}
            )
            if created:
                # Add relationships
                game.publishers.add(publisher)
                game.studios.add(studio)

                for platform_name in platforms_list:
                    platform, _ = Platform.objects.get_or_create(name=platform_name)
                    game.platforms.add(platform)
                    
                for genre_name in genres_list:
                    genre, _ = Genre.objects.get_or_create(name=genre_name, defaults={'description': ''})
                    game.genres.add(genre)

                self.stdout.write(self.style.SUCCESS(f"Imported game: {title}"))
            else:
                self.stdout.write(f"Game already exists: {title}")
