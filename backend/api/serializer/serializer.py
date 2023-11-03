# serializers.py
from api.models import *
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.utils import timezone

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class GenericUserPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = GenericUser
        fields = ['password']

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    

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

class OrganizerProfileSerializer(serializers.ModelSerializer):
    user = GenericUserSerializer()
    class Meta:
        model = Organizer
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
    def validate(self, attrs):
        if 'endDate' and 'startDate' in attrs:
            if attrs['endDate'] <= attrs['startDate']:
                raise serializers.ValidationError({"Start Date": "Start Date cannot be more than end date"})
        if 'noVol' in attrs:
            if attrs['noVol'] <= 0:
                raise serializers.ValidationError({"Number of volunteers": "Number of volunteers cannot less than 0"})
        return attrs

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

class AllEventOrganizerMappingSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    class Meta:
        model = EventOrganizerMapping
        fields = ["event"]

class EventOrganizerMappingCreate(serializers.ModelSerializer):
    class Meta:
        model = EventOrganizerMapping
        fields = '__all__'

class EventParticipantSerializer(serializers.ModelSerializer):
    participant = NormalUserSerializer()
    class Meta:
        model = EventParticipant
        fields = '__all__'

class EventSignUpParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = ['event','participant']
        validators = []

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
