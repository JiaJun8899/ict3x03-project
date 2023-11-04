import io
import datetime
import os
import glob
from django.conf import settings
from PIL import Image
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Event, GenericUser, Organizer, EventOrganizerMapping, NormalUser, EventParticipant, NOK, EmergencyContacts
from api.models.GenericUser import GenericUser
from django_otp.plugins.otp_email.models import EmailDevice
from django.utils import timezone
from dotenv import load_dotenv
load_dotenv()

class GetAllEventTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = GenericUser.objects.create_user(
            username='test@test.com',
            email='test@test.com',
            first_name='test',
            last_name='test',
            phoneNum='91234567',
            nric='567H',
            password='testiepassword',
        )
        self.test_org = Organizer.organizerManager.create(user_id=self.test_user.id)
        self.event = Event.eventManager.create(eventName="test Event", startDate="2023-10-13T04:34:00+08:00", endDate = timezone.now() + datetime.timedelta(days=2), eventImage = None, noVol= 1233, eventDesc=123123, eventStatus= "Open")
        self.eventMap = EventOrganizerMapping.eventMapperManager.create(event_id = self.event.eid, organizer_id = self.test_org.user_id, approval = "accepted")
        self.event1 = Event.eventManager.create(eventName="test Event1", startDate="2023-10-13T04:34:00+08:00", endDate = timezone.now() + datetime.timedelta(days=2), eventImage = None, noVol= 1233, eventDesc=123123, eventStatus= "Open")
        self.eventMap1 = EventOrganizerMapping.eventMapperManager.create(event_id = self.event1.eid, organizer_id = self.test_org.user_id, approval = "accepted")
        self.event2 = Event.eventManager.create(eventName="test Event2", startDate="2023-10-13T04:34:00+08:00", endDate = timezone.now() + datetime.timedelta(days=2), eventImage = None, noVol= 1233, eventDesc=123123, eventStatus= "Open")
        self.eventMap = EventOrganizerMapping.eventMapperManager.create(event_id = self.event2.eid, organizer_id = self.test_org.user_id, approval = "accepted")


    def test_all_events_Fail(self):
        url = reverse('get-all-events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_all_event(self):
        norm_generic = GenericUser.objects.create_user(
            username='test@norm.com',
            email='test@norm.com',
            first_name='test',
            last_name='test',
            phoneNum='91234567',
            nric='567H',
            password='testiepassword',
        )
        self.test_org = NormalUser.normalUserManager.create(user_id=norm_generic.id, birthday="2001-03-12")
        self.client.login(username="test@test.com", password="testiepassword")
        session = self.client.session
        session['role'] = "normal"
        session.save()
        url = reverse('get-all-events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)


class RegisterTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        org_generic = GenericUser.objects.create_user(
            username='test@org.com',
            email='test@org.com',
            first_name='test',
            last_name='test',
            phoneNum='91234567',
            nric='567H',
            password='testiepassword',
        )
        Organizer.organizerManager.create(user_id=org_generic.id)
        norm_generic = GenericUser.objects.create_user(
            username='test@normal.com',
            email='test@normal.com',
            first_name='test',
            last_name='test',
            phoneNum='91234567',
            nric='567H',
            password='testiepassword',
        )
        NormalUser.normalUserManager.create(user_id=norm_generic.id, birthday="2001-03-12")
    
    def test_create_Organizer(self):
        data = {"email": "jiajun@org.com", "firstName": "jiajun", "lastName": "jiajun", "phoneNum":91234567, "NRIC": "456h", "password": "jiajun123", "password2": "jiajun123","organization": True, "recaptchaValue": "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI", "SECRET_KEY":os.getenv("TEST_INPUT", os.environ.get("TEST_INPUT"))}
        url = reverse('register')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Organizer.organizerManager.getAllRecords()), 2)

    def test_create_Normal(self):
        data = {"email": "jiajun@normal.com", "firstName": "jiajun", "lastName": "jiajun", "phoneNum":91234567, "NRIC": "456h", "password": "jiajun123", "password2": "jiajun123","organization": False, "birthday": "2007-10-17", "recaptchaValue": "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI", "SECRET_KEY":os.getenv("TEST_INPUT", os.environ.get("TEST_INPUT"))}
        url = reverse('register')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(NormalUser.normalUserManager.getAllRecords()), 2)
    
    def test_create_Organizer_fail_inputs(self):
        data = {"email": "test@org.com", "firstName": "jiajun", "lastName": "jiajun", "phoneNum":912334567, "NRIC": "4456h", "password": "password", "password2": "password","organization": True, "recaptchaValue": "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI", "SECRET_KEY":os.getenv("TEST_INPUT", os.environ.get("TEST_INPUT"))}
        url = reverse('register')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 5)
    
    def test_Organizer_fail_special_char(self):
        data = {"email": "jiajun123@org.com", "firstName": "<jiajun", "lastName": "jiajun", "phoneNum":91234567, "NRIC": "456h", "password": "jiajun123", "password2": "jiajun123","organization": True, "recaptchaValue": "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI", "SECRET_KEY":os.getenv("TEST_INPUT", os.environ.get("TEST_INPUT"))}
        url = reverse('register')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_clash_create_Normal(self):
        data = {"email": "test@normal.com", "firstName": "jiajun", "lastName": "jiajun", "phoneNum":91234567, "NRIC": "456h", "password": "jiajun123", "password2": "jiajun123","organization": False, "birthday": "2007-10-17", "recaptchaValue": "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI", "SECRET_KEY":os.getenv("TEST_INPUT", os.environ.get("TEST_INPUT"))}
        url = reverse('register')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_Normal_fail_special_char(self):
        data = {"email": "jiajun@normal.com", "firstName": "jiajun", "lastName": "<jiajun", "phoneNum":91234567, "NRIC": "456h", "password": "jiajun123", "password2": "jiajun123","organization": False, "birthday": "2007-10-17", "recaptchaValue": "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI", "SECRET_KEY":os.getenv("TEST_INPUT", os.environ.get("TEST_INPUT"))}
        url = reverse('register')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class OrganizerTest(APITestCase):
    def generate_photo_file(self, width=100, height=100):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(width, height), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'testAPIIMAGE.png'
        file.seek(0)
        return file

    def setUp(self):
        self.client = APIClient()
        self.test_user = GenericUser.objects.create_user(
            username='test@test.com',
            email='test@test.com',
            first_name='test',
            last_name='test',
            phoneNum='91234567',
            nric='567H',
            password='testiepassword',
        )
        self.test_org = Organizer.organizerManager.create(user_id=self.test_user.id)
        self.event = Event.eventManager.create(eventName="test Event", startDate="2023-10-13T04:34:00+08:00", endDate = timezone.now() + datetime.timedelta(days=2), eventImage = None, noVol= 1233, eventDesc=123123, eventStatus= "Open")
        self.eventMap = EventOrganizerMapping.eventMapperManager.create(event_id = self.event.eid, organizer_id = self.test_org.user_id, approval = "accepted")
        self.client.login(username="test@test.com", password="testiepassword")
        session = self.client.session
        session['role'] = "Organizer"
        session.save()
    
    def test_create_event(self):
        photo_file = self.generate_photo_file()
        data = {"eventName": "Test Create", "startDate": timezone.now(),"endDate": timezone.now() + datetime.timedelta(days=2),"noVol": 12,"eventDesc": "This is for test","eventImage": photo_file}
        url = reverse('get-event-org')
        response = self.client.post(url, data)
        createdEvent = Event.eventManager.getAllRecords().filter(eventName="Test Create")
        createdEvent.update(eventStatus = "Open")
        createdEventMap = EventOrganizerMapping.eventMapperManager.getMapByEventUUID(createdEvent[0].eid)
        createdEventMap.approval = "accepted"
        createdEventMap.save()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('get-event-org')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)
    
    def test_create_event_fail_dates(self):
        photo_file = self.generate_photo_file()
        data = {"eventName": "Test Create", "startDate": timezone.now(),"endDate": timezone.now() - datetime.timedelta(days=2),"noVol": 12,"eventDesc": "This is for test","eventImage": photo_file}
        url = reverse('get-event-org')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_event_fail_image(self):
        photo_file = self.generate_photo_file(width=23000, height=23000)
        data = {"eventName": "Test Create", "startDate": timezone.now(),"endDate": timezone.now() + datetime.timedelta(days=2),"noVol": 12,"eventDesc": "This is for test","eventImage": photo_file}
        url = reverse('get-event-org')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_edit_event(self):
        photo_file = self.generate_photo_file()
        url = reverse('get-event-org')
        response = self.client.get(url)
        eid = response.data[0]['event']['eid']
        data = {"eid": eid, "eventName": "<Test Updated","eventImage": photo_file}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url)
        self.assertEqual(response.data[0]['event']['eventName'], "&lt;Test Updated")
    
    def test_edit_event_fail_date(self):
        url = reverse('get-event-org')
        response = self.client.get(url)
        eid = response.data[0]['event']['eid']
        data = {"eid": eid, "eventName": "<Test Updated", "endDate": "2023-10-10T04:34:00+08:00"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.get(url)
        self.assertEqual(response.data[0]['event']['eventName'], "test Event")
    
    def test_edit_event_fail_image(self):
        photo_file = self.generate_photo_file(width=23000, height=23000)
        url = reverse('get-event-org')
        response = self.client.get(url)
        eid = response.data[0]['event']['eid']
        data = {"eid": eid, "eventName": "<Test Updated","eventImage": photo_file}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_event(self):
        url = reverse('get-event-org')
        response = self.client.get(url)
        eid = response.data[0]['event']['eid']
        data = {"eid": eid}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)

    def tearDown(self):
        super().tearDown()
        media_root = settings.MEDIA_ROOT
        image_directory = os.path.join(media_root, 'events')
        image_files = glob.glob(os.path.join(image_directory, 'testAPIIMAGE*'))
        for image_file in image_files:
            if os.path.exists(image_file):
                os.remove(image_file)


class OrganizerTestInvalid(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = GenericUser.objects.create_user(
            username='test@test.com',
            email='test@test.com',
            first_name='test',
            last_name='test',
            phoneNum='91234567',
            nric='567H',
            password='testiepassword',
        )
        self.test_org = Organizer.organizerManager.create(user_id=self.test_user.id)
        self.event = Event.eventManager.create(eventName="test Event", startDate="2023-10-13T04:34:00+08:00", endDate = "2023-10-26T04:34:00+08:00", eventImage = None, eventStatus= "open", noVol= 1233, eventDesc=123123)
        self.eventMap = EventOrganizerMapping.eventMapperManager.create(event_id = self.event.eid, organizer_id = self.test_org.user_id)
        
        self.test_user_2 = GenericUser.objects.create_user(
            username='test12@test12.com',
            email='test12@test12.com',
            first_name='test',
            last_name='test',
            phoneNum='91234567',
            nric='567H',
            password='testiepassword',
        )
        self.test_org_2 = Organizer.organizerManager.create(user_id=self.test_user_2.id)
        self.client.login(username="test12@test12.com", password="testiepassword")
        session = self.client.session
        session['role'] = "organizer"
        session.save()
    
    def test_edit_event_fail(self):
        url = reverse('get-event-org')
        response = self.client.get(url)
        data = {"eid": self.event.eid, "eventName": "Test Updated"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_event(self):
        url = reverse('get-event-org')
        response = self.client.get(url)
        data = {"eid": self.event.eid}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LoginAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = GenericUser.objects.create_user(
            username='test@email.com',
            email='test@email.com',
            first_name='John',
            last_name='Doe',
            phoneNum='91234567',
            nric='567D',
            password='test_password',
        )

        cls.test_org = NormalUser.normalUserManager.create(user_id=cls.test_user.id, birthday="2001-03-12")
        cls.emailDevice = EmailDevice.objects.get_or_create(user=cls.test_user, email=cls.test_user.email,name="EMAIL")[0]

    def set_temp_id_in_session(self):
        session = self.client.session
        session['temp_id'] = str(self.test_user.id)
        session.save()

    def set_false_temp_id_in_session(self):
        session = self.client.session
        session['temp_id'] = str(self.test_user.id)[1:] + "1"
        session.save()

    def test_login_success(self):
        url = reverse('auth-login')
        data = {'username': 'test@email.com', 'password': 'test_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('temp_id', self.client.session)
        self.assertEqual(str(self.client.session['temp_id']), str(self.test_user.id))

    def test_login_failure(self):
        url = reverse('auth-login')
        data = {'username': 'test@email.com', 'password': 'wrong_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('temp_id', self.client.session)

    def test_get_otp_success(self):
        # Set the temp_id in session
        self.set_temp_id_in_session()
        url = reverse('auth-get-OTP')
        response = self.client.post(url, {}, format='json')  # No data needed in this case
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_otp_failure_no_temp_id_in_session(self):
        url = reverse('auth-get-OTP')
        response = self.client.post(url, {}, format='json')  # No data needed in this case
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_otp_failure_wrong_temp_id_in_session(self):
        url = reverse('auth-get-OTP')
        self.set_false_temp_id_in_session()
        response = self.client.post(url, {}, format='json')  # No data needed in this case
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_otp_wrong_uuid(self):
        url = reverse('auth-verify-OTP')
        self.set_false_temp_id_in_session()
        self.emailDevice.generate_challenge()
        data = {'OTP': self.emailDevice.token}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Something went wrong')  # Replace with your actual error message

    def test_verify_otp_wrong_otp(self):
        url = reverse('auth-verify-OTP')  # Replace with your URL name
        self.emailDevice.generate_challenge()
        self.set_temp_id_in_session()
        data = {'OTP': self.emailDevice.token[1:] + "1"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Something went wrong')  # Replace with your actual error message

    def test_verify_otp_no_uuid_in_session(self):
        url = reverse('auth-verify-OTP')
        self.emailDevice.generate_challenge()
        data = {'OTP': self.emailDevice.token}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Something went wrong')  # Replace with your actual error message
        self.assertNotIn('temp_id', self.client.session)

    def test_verify_logout_unAuth_User(self):
        url = reverse('auth-verify-OTP')
        response = self.client.post(url, {})
        self.assertNotIn('temp_id', self.client.session)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Something went wrong')  # Replace with your actual error message

class NormalUserTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = GenericUser.objects.create_user(
            username='test@test.com',
            email='test@test.com',
            first_name='test',
            last_name='test',
            phoneNum='91234567',
            nric='567H',
            password='testiepassword',
        )
        self.test_org = Organizer.organizerManager.create(user_id=self.test_user.id)
        self.event = Event.eventManager.create(eventName="test Event", startDate=timezone.now() + datetime.timedelta(days=1), endDate = timezone.now() + datetime.timedelta(days=2), eventImage = None, noVol= 1233, eventDesc=123123, eventStatus= "open")
        self.eventMap = EventOrganizerMapping.eventMapperManager.create(event_id = self.event.eid, organizer_id = self.test_org.user_id, approval = "accepted")
        self.event1 = Event.eventManager.create(eventName="test Event1", startDate="2023-10-13T04:34:00+08:00", endDate = timezone.now() + datetime.timedelta(days=2), eventImage = None, noVol= 1233, eventDesc=123123, eventStatus= "open")
        self.eventMap1 = EventOrganizerMapping.eventMapperManager.create(event_id = self.event1.eid, organizer_id = self.test_org.user_id, approval = "accepted")
        self.event2 = Event.eventManager.create(eventName="test Event2", startDate=timezone.now() + datetime.timedelta(days=1), endDate = timezone.now() + datetime.timedelta(days=3), eventImage = None, noVol= 1233, eventDesc=123123, eventStatus= "open")
        self.eventMap = EventOrganizerMapping.eventMapperManager.create(event_id = self.event2.eid, organizer_id = self.test_org.user_id, approval = "accepted")
        norm_generic = GenericUser.objects.create_user(
            username='test@normal1.com',
            email='test@normal1.com',
            first_name='test1',
            last_name='test1',
            phoneNum='91234568',
            nric='568H',
            password='testiepassword',
        )
        norm_user =  NormalUser.normalUserManager.create(user_id=norm_generic.id, birthday="2001-03-12")
        signup1 = EventParticipant.eventParticipantManager.create(event=self.event1, participant=norm_user)
        signup2 = EventParticipant.eventParticipantManager.create(event=self.event2,participant=norm_user)
        
        self.client.login(username="test@normal1.com", password="testiepassword")
        session = self.client.session
        session['role'] = "Normal"
        session.save()
    
    def test_get_profile(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profile']['user']['username'],"test@normal1.com")
        self.assertEqual(response.data['profile']['birthday'],"2001-03-12")
        self.assertEqual(response.data['profile']['user']["phoneNum"],"91234568")
    
    def test_get_all_events(self):
        url = reverse('get-all-events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),3)
        
    def test_get_past_events(self):
        url = reverse('get-past-events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)

    def test_get_upcoming_events(self):
        url = reverse('get-upcoming-events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)

    def test_signup_event(self):
        url = reverse("event-sign-up")
        data = {
            'eid' :self.event.eid,
        }
        response = self.client.post(url,data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('get-upcoming-events')
        response = self.client.get(url)
        self.assertEqual(len(response.data),2)

    def test_cancel_event(self):
        url = reverse('get-upcoming-events')
        response = self.client.get(url)
        self.assertEqual(len(response.data),1)
        event = Event.eventManager.filter(eventName="test Event2")
        url = reverse("cancel-sign-up-event")
        data = {
            'eid' : event.first().eid,
        }
        response = self.client.delete(url,data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('get-upcoming-events')
        response = self.client.get(url)
        self.assertEqual(len(response.data),0)
        
    def test_get_event(self):
        event = Event.eventManager.filter(eventName="test Event1").first()
        url = reverse('get-event',args=[event.eid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile(self):
        nok = NOK.objects.create(name="bro", relationship="brother",phoneNum="84839585")
        
        url = reverse('profile')
        response = self.client.get(url)    
        data ={
            "first_name": "John",
            "last_name": "Doe",
            "email": response.data['profile']['user']["email"],
            "phoneNum": response.data['profile']['user']["phoneNum"],
            "userName": response.data['profile']['user']["username"],
            "nokName":nok.name,
            "nokRelationship":nok.relationship,
            "nokPhone":nok.phoneNum                
        }
        url = reverse('update-user-details')
        response = self.client.put(url,data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.data['nok']['name'],"bro")
        self.assertEqual(response.data['profile']['user']["first_name"],"John")
        
    def test_verify_logout_auth_User(self):
        url = reverse('auth-verify-OTP')
        self.client.login(username="test@email.com", password="test_password")
        response = self.client.post(url, {})
        self.assertNotIn('temp_id', self.client.session)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Something went wrong')

class ResetAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = GenericUser.objects.create_user(
            username='test@email.com',
            email='test@email.com',
            first_name='JohnJohn',
            last_name='Doe',
            phoneNum='91234567',
            nric='567D',
            password='test_password',
        )
        cls.test_org = NormalUser.normalUserManager.create(user_id=cls.test_user.id, birthday="2001-03-12")

    def setUp(self):
        self.url = reverse('auth-change-password')
        self.client.login(username="test@email.com", password="test_password")
        self.updateEmailDevice()

    def updateEmailDevice(self):
        self.emailDevice, created = EmailDevice.objects.get_or_create(
            user=self.test_user, 
            email=self.test_user.email,
            name="EMAIL"
        )

    def test_post_method_success(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'OTP HAS BEEN Sent')
        self.updateEmailDevice()
        self.assertNotEqual(self.emailDevice.token, None)

    def test_post_method_fail(self):
        self.client.logout()  # Simulating not logged-in user
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # self.assertEqual(response.data['detail'], 'Invalid Permission')
        self.updateEmailDevice()
        self.assertEqual(self.emailDevice.token, None)

    def test_put_method_password_change_success(self):
        self.updateEmailDevice()
        self.emailDevice.generate_challenge()
        data = {
            'currentPassword': 'test_password',
            'newPassword': 'new_password',
            'newPasswordConfirmation': 'new_password',
            'OTP': self.emailDevice.token
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.data['detail'], 'Password changed successfully')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Optionally, you can reload the user and check if the password actually changed
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.check_password('new_password'))

    def test_put_method_missing_fields(self):
        self.updateEmailDevice()
        self.emailDevice.generate_challenge()
        # Missing 'OTP' and 'newPasswordConfirmation'
        data = {'current Password': 'test_password', 'newPassword': 'new_password'}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Missing fields')

    def test_put_method_wrong_current_password(self):
        self.updateEmailDevice()
        self.emailDevice.generate_challenge()
        data = {
            'currentPassword': 'wrong_password',  # Wrong current password
            'newPassword': 'new_password',
            'newPasswordConfirmation': 'new_password',
            'OTP': self.emailDevice.token
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.data['detail'], 'Invalid current password')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_method_mismatch_new_passwords(self):
        self.updateEmailDevice()
        self.emailDevice.generate_challenge()
        data = {
            'currentPassword': 'test_password',
            'newPassword': 'new_password',
            'newPasswordConfirmation': 'another_password',  # Mismatched new password
            'OTP': self.emailDevice.token
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Passwords do not match')

    def test_put_method_invalid_otp(self):
        self.updateEmailDevice()
        self.emailDevice.generate_challenge()
        data = {
            'currentPassword': 'test_password',
            'newPassword': 'new_password',
            'newPasswordConfirmation': 'new_password',
            'OTP': 'wrong_otp'  # Invalid OTP
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid current password')

    def test_put_method_unauthorized_user(self):
        self.client.logout()  # Logging out to simulate unauthorized user
        self.updateEmailDevice()
        self.emailDevice.generate_challenge()
        data = {
            'currentPassword': 'test_password',
            'newPassword': 'new_password',
            'newPasswordConfirmation': 'new_password',
            'OTP': self.emailDevice.token
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # self.assertEqual(response.data['detail'], 'Unauthorized')

    def test_put_method_bad_password_allNumber(self):
        self.updateEmailDevice()
        self.emailDevice.generate_challenge()
        
        bad_passwords = ['123456789','JohnJohn','12@J','qwerty1234']
        bad_password = bad_passwords[0]
        data = {
            'currentPassword': 'test_password',
            'newPassword':bad_password,
            'newPasswordConfirmation':bad_password,
            'OTP': self.emailDevice.token
        }
        response = self.client.put(self.url, data)
        self.assertIn('ErrorDetail', str(response.data['detail']))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_method_bad_password_tooSimilar(self):
        self.updateEmailDevice()
        self.emailDevice.generate_challenge()
        
        bad_password = 'JohnJohn'
        data = {
            'currentPassword': 'test_password',
            'newPassword':bad_password,
            'newPasswordConfirmation':bad_password,
            'OTP': self.emailDevice.token
        }
        response = self.client.put(self.url, data)
        self.assertIn('ErrorDetail', str(response.data['detail']))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_method_bad_password_too_short(self):
        self.updateEmailDevice()
        self.emailDevice.generate_challenge()
        
        bad_password = "12@ABC"
        data = {
            'currentPassword': 'test_password',
            'newPassword':bad_password,
            'newPasswordConfirmation':bad_password,
            'OTP': self.emailDevice.token
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('ErrorDetail', str(response.data['detail']))

    def test_put_method_bad_password_too_common(self):
        self.updateEmailDevice()
        self.emailDevice.generate_challenge()
        
        bad_password = "qwerty123"
        data = {
            'currentPassword': 'test_password',
            'newPassword':bad_password,
            'newPasswordConfirmation':bad_password,
            'OTP': self.emailDevice.token
        }
        response = self.client.put(self.url, data)
        self.assertIn('ErrorDetail', str(response.data['detail']))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class ResetPasswordAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = GenericUser.objects.create_user(
            username='test@email.com',
            email='test@email.com',
            first_name='JohnJohn',
            last_name='Doe',
            phoneNum='91234567',
            nric='567D',
            password='test_password',
        )
        cls.test_org = NormalUser.normalUserManager.create(user_id=cls.test_user.id, birthday="2001-03-12")

    def setUp(self):
        self.url = reverse('auth-reset-password')  # Replace with your URL name for Reset Password
        self.updateEmailDevice()

    def updateEmailDevice(self,toGenerate=True):
        self.emailDevice, created = EmailDevice.objects.get_or_create(
            user=self.test_user, 
            email=self.test_user.email,
            name="EMAIL"
        )
        if toGenerate:
            self.emailDevice.generate_challenge()

    def test_post_method_success(self):
        data = {'email': 'test@email.com'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'email should be sent')
        self.updateEmailDevice()
        self.assertNotEqual(self.emailDevice.token, None)

    def test_put_method_password_reset_success(self):
        self.updateEmailDevice()
        self.emailDevice.generate_challenge()
        data = {
            'OTP': self.emailDevice.token,
            'email': 'test@email.com',
            'newPassword': 'new_password',
            'newPasswordConfirmation': 'new_password',
        }
        response = self.client.put(self.url, data)
        self.assertTrue(self.client.login(username='test@email.com', password='new_password'))
        self.assertFalse(self.client.login(username='test@email.com', password='fake_password'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Password changed successfully')

    def test_put_method_passwords_do_not_match(self):
        self.updateEmailDevice()
        self.emailDevice.generate_challenge()
        data = {
            'OTP': self.emailDevice.token,
            'email': 'test@email.com',
            'newPassword': 'new_password',
            'newPasswordConfirmation': 'wrong_password',
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Passwords do not match')

    def test_put_method_wrong_otp(self):
        self.updateEmailDevice()
        data = {
            'OTP': self.emailDevice.token[1:] + "1",
            'email': 'test@email.com',
            'newPassword': 'new_password',
            'newPasswordConfirmation': 'new_password',
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Something went wrong')

    def test_put_method_invalid_email(self):
        self.updateEmailDevice()
        self.emailDevice.generate_challenge()
        data = {
            'OTP': self.emailDevice.token,
            'email': 'wrong@email.com',
            'newPassword': 'new_password',
            'newPasswordConfirmation': 'new_password',
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Something went wrong')
