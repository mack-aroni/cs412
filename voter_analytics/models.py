from django.db import models
import csv

class Voter(models.Model):
    #voter_id = models.CharField(max_length=20, unique=True)
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.CharField(max_length=10)
    street_name = models.TextField()
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


def load_data():
    '''Function to load data records from CSV file into Django model instances.'''

    # Delete existing records to prevent duplicates:
    Voter.objects.all().delete()
    
    csv_filepath = 'voter_analytics/newton_voters.csv'
    
    with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
        headers = csvfile.readline().strip().split(',')
        
        for line in csvfile:
            fields = line.strip().split(',')
            row = dict(zip(headers, fields))
            
            try:
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
                    v20state=row['v20state'].strip().upper() == 'TRUE',
                    v21town=row['v21town'].strip().upper() == 'TRUE',
                    v21primary=row['v21primary'].strip().upper() == 'TRUE',
                    v22general=row['v22general'].strip().upper() == 'TRUE',
                    v23town=row['v23town'].strip().upper() == 'TRUE',
                    voter_score=int(row['voter_score'])
                )
                voter.save()
                print(f'Created voter: {voter}')
            except Exception as e:
                print(f"Skipped: {row} due to {e}")
    
    print(f'Done. Created {Voter.objects.count()} voter records.')
