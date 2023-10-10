# serializers.py
from api.models import *
from rest_framework import serializers

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class EmergencyContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContacts
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventOrganizerMappingSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    organizer = serializers.StringRelatedField()
    class Meta:
        model = EventOrganizerMapping
        fields = ["event", "organizer"]

class EventParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = '__all__'

class GenericUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericUser
        fields = '__all__'

class NOKSerializer(serializers.ModelSerializer):
    class Meta:
        model = NOK
        fields = '__all__'

class NormalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalUser
        fields = '__all__'

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'
