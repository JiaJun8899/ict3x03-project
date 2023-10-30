import io
import datetime
import os
import glob
from django.conf import settings
from PIL import Image
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Event, GenericUser, Organizer, EventOrganizerMapping, NormalUser
from api.models.GenericUser import GenericUser
from django_otp.plugins.otp_email.models import EmailDevice
from django.utils import timezone
from dotenv import load_dotenv
load_dotenv()

class GetAllEventTest(APITestCase):
    def setUp(self):
        Event.eventManager.create(eventName="test Event", startDate="2023-10-13T04:34:00+08:00", endDate = "2023-10-26T04:34:00+08:00", eventImage = None, eventStatus= "open", noVol= 1233, eventDesc=123123)
        Event.eventManager.create(eventName="test Event1", startDate="2023-10-13T04:34:00+08:00", endDate = "2023-10-26T04:34:00+08:00", eventImage = None, eventStatus= "open", noVol= 1233, eventDesc=123123)
        Event.eventManager.create(eventName="test Event2", startDate="2023-10-13T04:34:00+08:00", endDate = "2023-10-26T04:34:00+08:00", eventImage = None, eventStatus= "open", noVol= 1233, eventDesc=123123)

    def test_all_events(self):
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
            nric='S1234567H',
            password='testiepassword',
        )
        Organizer.organizerManager.create(user_id=org_generic.id)
        norm_generic = GenericUser.objects.create_user(
            username='test@normal.com',
            email='test@normal.com',
            first_name='test',
            last_name='test',
            phoneNum='91234567',
            nric='S1234567H',
            password='testiepassword',
        )
        NormalUser.normalUserManager.create(user_id=norm_generic.id, birthday="2001-03-12")
    
    def test_create_Organizer(self):
        data = {"email": "jiajun@org.com", "firstName": "jiajun", "lastName": "jiajun", "phoneNum":91234567, "NRIC": "s9123456h", "password": "jiajun123", "password2": "jiajun123","organization": True, "recaptchaValue": "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI", "SECRET_KEY":os.getenv("TEST_INPUT", os.environ.get("TEST_INPUT"))}
        url = reverse('register')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Organizer.organizerManager.getAllRecords()), 2)

    def test_create_Normal(self):
        data = {"email": "jiajun@normal.com", "firstName": "jiajun", "lastName": "jiajun", "phoneNum":91234567, "NRIC": "s9123456h", "password": "jiajun123", "password2": "jiajun123","organization": False, "birthday": "2007-10-17", "recaptchaValue": "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI", "SECRET_KEY":os.getenv("TEST_INPUT", os.environ.get("TEST_INPUT"))}
        url = reverse('register')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(NormalUser.normalUserManager.getAllRecords()), 2)
    
    def test_clash_create_Organizer(self):
        data = {"email": "test@org.com", "firstName": "jiajun", "lastName": "jiajun", "phoneNum":91234567, "NRIC": "s9123456h", "password": "jiajun123", "password2": "jiajun123","organization": True, "recaptchaValue": "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI", "SECRET_KEY":os.getenv("TEST_INPUT", os.environ.get("TEST_INPUT"))}
        url = reverse('register')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_clash_create_Normal(self):
        data = {"email": "test@normal.com", "firstName": "jiajun", "lastName": "jiajun", "phoneNum":91234567, "NRIC": "s9123456h", "password": "jiajun123", "password2": "jiajun123","organization": False, "birthday": "2007-10-17", "recaptchaValue": "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI", "SECRET_KEY":os.getenv("TEST_INPUT", os.environ.get("TEST_INPUT"))}
        url = reverse('register')
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

class OrganizerTest(APITestCase):
    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
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
            nric='S1234567H',
            password='testiepassword',
        )
        self.test_org = Organizer.organizerManager.create(user_id=self.test_user.id)
        event = Event.eventManager.create(eventName="test Event", startDate="2023-10-13T04:34:00+08:00", endDate = "2023-10-26T04:34:00+08:00", eventImage = None, eventStatus= "open", noVol= 1233, eventDesc=123123)
        self.eventMap = EventOrganizerMapping.eventMapperManager.create(event_id = event.eid, organizer_id = self.test_org.user_id)
        self.client.login(username="test@test.com", password="testiepassword")
        session = self.client.session
        session['role'] = "organizer"
        session.save()
    
    def test_create_event(self):
        photo_file = self.generate_photo_file()
        data = {"eventName": "Test Create", "startDate": timezone.now(),"endDate": timezone.now() + datetime.timedelta(days=2),"noVol": 12,"eventDesc": "This is for test","eventImage": photo_file}
        url = reverse('get-event-org')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('get-event-org')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)
    
    def test_edit_event(self):
        photo_file = self.generate_photo_file()
        url = reverse('get-event-org')
        response = self.client.get(url)
        eid = response.data[0]['event']['eid']
        data = {"eid": eid, "eventName": "Test Updated","eventImage": photo_file}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url)
        self.assertEqual(response.data[0]['event']['eventName'], "Test Updated")
    
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


class LoginAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = GenericUser.objects.create_user(
            username='test@email.com',
            email='test@email.com',
            first_name='John',
            last_name='Doe',
            phoneNum='91234567',
            nric='S1234567D',
            password='test_password',
        )

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


    def test_verify_otp_success(self):
        url = reverse('auth-verify-OTP')  # Replace with your URL name
        self.emailDevice.generate_challenge()
        self.set_temp_id_in_session()
        data = {'OTP': self.emailDevice.token}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'OTP is Correct')

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