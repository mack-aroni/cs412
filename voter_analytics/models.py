# File: models.py
# Author: Ethan Machleder (emach@bu.edu) May 3, 2025
# Description: This file defines the data model and import logic for the voter analytics application.
# The Voter model represents individual voter records, including personal information,
# address, registration details, voting history, and a derived voter score.
# A helper function `load_data` is included to populate the database from a CSV file.

from django.db import models
import csv

class Voter(models.Model):
    '''Encapsulate the data for an individual voter record'''

    # Personal information
    last_name = models.TextField()               # Last name of the voter
    first_name = models.TextField()              # First name of the voter
    date_of_birth = models.DateField()           # Date of birth (YYYY-MM-DD)

    # Address fields
    street_number = models.CharField(max_length=10)          # Street number (e.g., "42")
    street_name = models.TextField()                         # Street name (e.g., "Maple Ave")
    apartment_number = models.CharField(
        max_length=10, blank=True, null=True
    )                                                        # Optional apartment number
    zip_code = models.CharField(max_length=10)               # ZIP code

    # Registration and party
    date_of_registration = models.DateField()                # Date when the voter registered
    party_affiliation = models.CharField(max_length=2)       # Political party (e.g., "D", "R", "U")
    precinct_number = models.CharField(max_length=10)        # Voting precinct

    # Voting history (1 if voted, 0 otherwise)
    v20state = models.IntegerField()     # 2020 State Election participation
    v21town = models.IntegerField()      # 2021 Town Election participation
    v21primary = models.IntegerField()   # 2021 Primary participation
    v22general = models.IntegerField()   # 2022 General Election participation
    v23town = models.IntegerField()      # 2023 Town Election participation

    # Aggregate voting behavior score
    voter_score = models.IntegerField()  # Computed score from 0–5

    def __str__(self):
        '''Return a string representation of this voter'''
        return f"{self.first_name} {self.last_name}"


def load_data():
    '''
    Load voter records from a CSV file and save them to the database.
    If data already exists, it is deleted before loading fresh records.
    '''

    # Remove all existing Voter records to avoid duplication
    Voter.objects.all().delete()

    # Path to the CSV file (should be placed under voter_analytics/)
    csv_filepath = 'voter_analytics/newton_voters.csv'

    with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
        # Read the first line of the file to get header column names
        headers = csvfile.readline().strip().split(',')

        # Iterate over the remaining lines in the CSV file
        for line in csvfile:
            fields = line.strip().split(',')
            row = dict(zip(headers, fields))  # Map column names to values

            try:
                # Construct and save a Voter instance
                voter = Voter(
                    last_name=row['Last Name'],
                    first_name=row['First Name'],
                    street_number=row['Residential Address - Street Number'],
                    street_name=row['Residential Address - Street Name'],
                    apartment_number=row['Residential Address - Apartment Number'] if row['Residential Address - Apartment Number'] else None,
                    zip_code=row['Residential Address - Zip Code'],
                    date_of_birth=row['Date of Birth'],
                    date_of_registration=row['Date of Registration'],
                    party_affiliation=row['Party Affiliation'].strip(),
                    precinct_number=row['Precinct Number'],
                    v20state=1 if row['v20state'].strip().upper() == 'TRUE' else 0,
                    v21town=1 if row['v21town'].strip().upper() == 'TRUE' else 0,
                    v21primary=1 if row['v21primary'].strip().upper() == 'TRUE' else 0,
                    v22general=1 if row['v22general'].strip().upper() == 'TRUE' else 0,
                    v23town=1 if row['v23town'].strip().upper() == 'TRUE' else 0,
                    voter_score=int(row['voter_score'])
                )
                voter.save()
                print(f'Created voter: {voter}')
            except Exception as e:
                # Skip malformed or incomplete records
                print(f"Skipped: {row} due to {e}")

    # Output total number of successfully loaded records
    print(f'Done. Created {Voter.objects.count()} voter records.')
