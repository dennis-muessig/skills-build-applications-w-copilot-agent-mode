mongosh --quiet --eval 'db = db.getSiblingDB("octofit_db"); db.getCollectionNames().forEach(function(c){print(c);printjson(db[c].findOne())})'from django.core.management.base import BaseCommand
from django.conf import settings
from pymongo import MongoClient, ASCENDING

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email
        db.users.create_index([('email', ASCENDING)], unique=True)

        # Teams
        teams = [
            {'name': 'Marvel'},
            {'name': 'DC'}
        ]
        db.teams.insert_many(teams)

        # Users
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'Marvel'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'DC'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'DC'}
        ]
        db.users.insert_many(users)

        # Activities
        activities = [
            {'user': 'Iron Man', 'activity': 'Running', 'duration': 30},
            {'user': 'Batman', 'activity': 'Cycling', 'duration': 45},
            {'user': 'Wonder Woman', 'activity': 'Swimming', 'duration': 60},
            {'user': 'Captain America', 'activity': 'Rowing', 'duration': 25}
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'team': 'Marvel', 'points': 120},
            {'team': 'DC', 'points': 105}
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'user': 'Iron Man', 'workout': 'Pushups', 'reps': 50},
            {'user': 'Batman', 'workout': 'Pullups', 'reps': 30},
            {'user': 'Wonder Woman', 'workout': 'Squats', 'reps': 40},
            {'user': 'Captain America', 'workout': 'Lunges', 'reps': 35}
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))

        # Test query
        self.stdout.write('Testing query...')
        db = db.getSiblingDB("octofit_db")
        db.getCollectionNames().forEach(function(c){print(c);printjson(db[c].findOne())})
