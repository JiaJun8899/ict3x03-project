from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import NormalUser, Event, GenericUser


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