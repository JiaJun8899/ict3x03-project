# serializers.py
from api.models import *
from rest_framework import serializers

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class GenericUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericUser
        fields = ['first_name', 'last_name', 'email', 'phoneNum']

class NOKSerializer(serializers.ModelSerializer):
    class Meta:
        model = NOK
        fields = '__all__'

class NormalUserSerializer(serializers.ModelSerializer):
    user = GenericUserSerializer()
    class Meta:
        model = NormalUser
        fields = '__all__'

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EmergencyContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContacts
        fields = '__all__'


class EventOrganizerMappingSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    organizer = serializers.StringRelatedField()
    class Meta:
        model = EventOrganizerMapping
        fields = ["event", "organizer"]

class EventOrganizerMappingCreate(serializers.ModelSerializer):
    class Meta:
        model = EventOrganizerMapping
        fields = '__all__'

class EventParticipantSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    participant = NormalUserSerializer()
    class Meta:
        model = EventParticipant
        fields = ['event','participant']