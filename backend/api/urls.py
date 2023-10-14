from django.urls import path
from . import views

urlpatterns = [
    path('update-organizer-status/', views.UpdateOrganizerStatus.as_view(), name='update_organizer_status'),
    path('get-all-organizers/', views.GetAllOrganizers.as_view(), name='get_all_organizers'),
    path('get-all-events/', views.EventAPI.as_view(), name='get-all-events'),
    path('get-event-byorg/<str:organization_id>/', views.EventsByOrganizationAPI.as_view(), name='get-event-org'),
    path('get-single-event/<str:organization_id>/<str:event_id>', views.EventSingleByOrganizationAPI.as_view(), name='get-single-event'),
    path('register',views.RegisterUserAPIView.as_view()),
    path('update-user-details/',views.UpdateUserAPIView.as_view()),
    path('sign-up-event/',views.SignUpEventAPIView.as_view()), 
    path('profile/<str:user_id>/',views.GetProfileDetailsAPIView.as_view(), name="get-profile"),       
    path('search-events/', views.SearchEvents.as_view())
]