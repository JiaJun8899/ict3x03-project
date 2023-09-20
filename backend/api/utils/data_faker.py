from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils import timezone
from api.models import GenericUser, Admin, NormalUser, Organizer, Event, NOK, EmergencyContacts, EventOrganizerMapping, EventParticipant
from faker import Faker
import random
import os

# Initialize the faker instance
fake = Faker()
Faker.seed(12334)

# Configure Django settings to run the script standalone
import django
django.setup()

def generate_8_digit_phone():
    return str(random.randint(10000000, 99999999))

def generate_singapore_nric():
    first_letter = random.choice(["S", "T", "F", "G"])
    digits = [random.randint(0, 9) for _ in range(7)]
    last_letter = random.choice("ABCDEFGHIZJ")
    nric = f"{first_letter}{''.join(map(str, digits))}{last_letter}"
    return nric

def create_generic_users(num):
    User = get_user_model()
    for _ in range(num):
        random_choice = random.choice(['normal','organizer'])
        username = fake.user_name()
        if not User.objects.filter(username=username).exists():
            user = User.objects.create(username=username, first_name=fake.first_name(), last_name=fake.last_name(),phone=generate_8_digit_phone(), 
                                       nric=generate_singapore_nric(),auth=random_choice, email=username+"@gmail.com",)
            user.set_password("test_password")
            user.save()

def create_admins():
    for user in GenericUser.objects.filter(auth='admin'):
        Admin.objects.create(user=user)


def create_normal_users():
    for user in GenericUser.objects.filter(auth='normal'):
        NormalUser.objects.create(user=user, birthday=timezone.now().date())


def create_organizers():
    for user in GenericUser.objects.filter(auth='organizer'):
        Organizer.objects.create(user=user, isApproved=True)


def create_events(num):
    for _ in range(num):
        Event.objects.create(
            name=fake.company(),
            startDatetime=timezone.now(),
            endDatetime=timezone.now() + timezone.timedelta(days=2),
            status='open',
            participant_limit=random.randint(50, 200),
            numberOfVolunteers =random.randint(5, 50),
            approval=True,
            description=fake.text()
        )

def create_NOKs(num):
    for _ in range(num):
        NOK.objects.create(
            fname=fake.first_name(),
            lname=fake.last_name(),
            relationship=fake.random_element(['Father', 'Child' , 'Mother', 'Sibling', 'Spouse']),
            phone=generate_8_digit_phone(),
            email=fake.email(),
            age=str(random.randint(20, 60))
        )


def create_emergency_contacts():
    all_normal_users = NormalUser.objects.all()
    all_nok = NOK.objects.all()

    nok_count = len(all_nok)

    for normal_user in all_normal_users:
        selected_nok = all_nok[random.randint(0, nok_count - 1)]
        try:
            EmergencyContacts.objects.create(
                normalUser=normal_user, 
                nok=selected_nok
            )
        except Exception as e:
            print(f"Failed to create EmergencyContacts for NormalUser ID: {normal_user.user_id}. Error: {e}")


def create_event_organizer_mappings():
    try:
        for event in Event.objects.all():
            for organizer in Organizer.objects.all():
                # Check for existing mapping
                existing_mapping = EventOrganizerMapping.objects.filter(event=event, organizer=organizer).exists()

                if not existing_mapping:
                    EventOrganizerMapping.objects.create(event=event, organizer=organizer)

    except Exception as e:
        print(f"An error occurred: {e}")

def create_event_participants():
    for event in Event.objects.all():
        for normal_user in NormalUser.objects.all():
            EventParticipant.objects.create(event=event, participant=normal_user)

@transaction.atomic
def runfile():
    try:
        print("Creating fake data...")
        
        # Your data creation functions go here
        create_generic_users(100)
        create_admins()
        create_normal_users()
        create_organizers()
        create_events(10)
        create_NOKs(10)
        create_emergency_contacts()
        create_event_organizer_mappings()
        create_event_participants()
        
        print("Fake data creation complete!")
    except Exception as e:
        print(f"An error occurred: {e}")
        # The transaction will be rolled back
        raise e
if __name__ == "__main__":
    runfile()
