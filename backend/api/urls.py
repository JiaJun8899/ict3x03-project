from django.urls import path
from . import views

urlpatterns = [
    path('update-organizer-status/', views.UpdateOrganizerStatus.as_view(), name='update_organizer_status'),
    path('get-all-organizers/', views.GetAllOrganizers.as_view(), name='get_all_organizers'),
    path('get-all-events/', views.EventAPI.as_view(), name='get-all-events'),
    path('get-event-byorg/', views.EventsByOrganizationAPI.as_view(), name='get-event-org'),
    path('get-single-event/<str:event_id>', views.EventSingleByOrganizationAPI.as_view(), name='get-single-event'),
    path('register',views.RegisterUserAPIView.as_view(), name="register"),
    path('update-user-details/',views.UpdateUserAPIView.as_view(), name="update-user-details"),
    path('sign-up-event/',views.SignUpEventAPIView.as_view(), name="event-sign-up"),
    path('cancel-sign-up-event/',views.CancelSignUpEventAPIView.as_view()),  
    path('profile/',views.GetProfileDetailsAPIView.as_view(), name="get-profile"),       
    path('search-events/', views.SearchEvents.as_view(), name="serach-events"),
    path('test',views.TestAPI.as_view()),
    path('get-all-events/', views.GetAllEvent.as_view(), name='get_all_events'),
    path('get-event/<str:eid>',views.GetEvent.as_view(), name='get-event'),
    path('auth-login/', views.Login.as_view(), name='login'),
    path('csrf/', views.csrf, name='get-csrf'),
    path('get-all-events/', views.GetAllEvent.as_view(), name='get-all-events'),
    path('auth-login/', views.Login.as_view(), name='get-all-events'),
    path('auth-verify-OTP/', views.VerifyOtp.as_view(), name='verify-OTP'),
    path('auth-get-OTP/', views.GetOTP.as_view(), name='get-OTP'),
    path('auth-logout/', views.Logout.as_view(), name='logout'),
]

