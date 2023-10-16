from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils import timezone
from api.models import GenericUser, Admin, NormalUser, Organizer, Event, NOK, EmergencyContacts, EventOrganizerMapping, EventParticipant
from faker import Faker
import random
import os

# Initialize the faker instance
fake = Faker()
Faker.seed(14434)


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

def create_generic_users():
    User = get_user_model()
    username = fake.user_name() + "_" + str(random.randint(0,999999))
    if not User.objects.filter(username=username).exists():
        user = User(username=username, first_name=fake.first_name(), last_name=fake.last_name(),phoneNum=generate_8_digit_phone(), 
                                   nric=generate_singapore_nric(), email=username+"@gmail.com",)
        user.set_password("test_password")
        user.save()
        return user
    return None

def create_admins():
    user = create_generic_users()
    if(user == None):
        print("USER IS NONE")
        return
    Admin.adminManager.create(user=user)


def create_normal_users(num):
    for _ in range(num):
        user = create_generic_users()
        if user == None:
            continue
        NormalUser.normalUserManager.create(user=user,birthday=fake.date())


def create_organizers(num):
    for _ in range(num):
        user = create_generic_users()
        if user == None:
            continue
        Organizer.organizerManager.create(user=user,validOrganisation =True)

def create_events(num):
    for _ in range(num):
        Event.eventManager.create(
            eventName=fake.company(),
            startDate=timezone.now(),
            endDate=timezone.now() + timezone.timedelta(days=2),
            eventStatus='open',
            noVol=random.randint(10, 5000),
            eventDesc =fake.text()
        )

def create_NOKs(num):
    for _ in range(num):
        NOK.objects.create(
            name=fake.first_name(),
            relationship=fake.random_element(['Father', 'Child' , 'Mother', 'Sibling', 'Spouse']),
            phoneNum=generate_8_digit_phone(),
        )


def create_emergency_contacts():
    all_normal_users = NormalUser.normalUserManager.exclude(emergencycontacts__isnull=False)
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
        for event in Event.eventManager.all():
            for organizer in Organizer.organizerManager.all():
                # Check for existing mapping
                existing_mapping = EventOrganizerMapping.objects.filter(event=event, organizer=organizer).exists()

                if not existing_mapping:
                    EventOrganizerMapping.objects.create(event=event, organizer=organizer)

    except Exception as e:
        print(f"An error occurred: {e}")

def create_event_participants():
    for event in Event.eventManager.all():
        for normal_user in NormalUser.normalUserManager.all():
            EventParticipant.objects.get_or_create(event=event, participant=normal_user)

@transaction.atomic
def runfile():
    try:
        print("Creating fake data...")
        
        # Your data creation functions go here
        create_admins()
        create_normal_users(100)
        create_organizers(100)
        create_events(100)
        create_NOKs(30)
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