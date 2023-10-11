# serializers.py
from api.models import *
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class GenericUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericUser
        fields = ['first_name', 'last_name', 'email', 'phoneNum', 'username']

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

class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=GenericUser.genericUserManager.getAllRecords())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = GenericUser
        fields = ('username','email', 'first_name', 'last_name', 'password', 'password2', 'nric', 'phoneNum')
        extra_kwargs = {'first_name': {'required': True},'last_name': {'required': True}, 'nric':{'required': True}}
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    def create(self, validated_data):
        user = GenericUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phoneNum = validated_data['phoneNum'],
            nric = validated_data['nric'],
            password = validated_data['password']
            )
        user.set_password(validated_data['password'])
        user.save()
        return user

class RegisterNormalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalUser
        fields = '__all__'