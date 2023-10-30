from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import NormalUser, Event, GenericUser
from api.models.GenericUser import GenericUser
from django_otp.plugins.otp_email.models import  EmailDevice

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

class CreateEventTest(APITestCase):
    def setUp(self):
        print("Hello")
        print(self.all_events)
    
    def test_create_event(self):
        Event.eventManager.create(eventName="test Event", startDate="2023-10-13T04:34:00+08:00", endDate = "2023-10-26T04:34:00+08:00", eventImage = None, eventStatus= "open", noVol= 1233, eventDesc=123123)
        self.assertEqual(True, True)

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

