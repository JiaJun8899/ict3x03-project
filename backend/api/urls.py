from django.urls import path
from . import views

urlpatterns = [
    path('update-organizer-status/', views.UpdateOrganizerStatus.as_view(), name='update_organizer_status'),
    path('get-all-organizers/', views.GetAllOrganizers.as_view(), name='get_all_organizers'),
    path('get-all-events/', views.EventAPI.as_view(), name='get-all-events')
]