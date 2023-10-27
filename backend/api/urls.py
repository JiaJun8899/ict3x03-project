from django.urls import path
from . import views

urlpatterns = [
    path('update-organizer-status/', views.UpdateOrganizerStatus.as_view(), name='update_organizer_status'), #admin, log
    path('get-all-organizers/', views.GetAllOrganizers.as_view(), name='get_all_organizers'), #admin, log
    path('get-all-events/', views.EventAPI.as_view(), name='get-all-events'), #users, don't log
    path('get-event-byorg/', views.EventsByOrganizationAPI.as_view(), name='get-event-org'), #organizer, don't log
    path('get-single-event/<str:event_id>', views.EventSingleByOrganizationAPI.as_view(), name='get-single-event'), #user|org, don't log
    path('register/',views.RegisterUserAPIView.as_view(), name="register"), #user|org, log
    path('update-user-details/',views.UpdateUserAPIView.as_view(), name="update-user-details"), #user|org, log
    path('sign-up-event/',views.SignUpEventAPIView.as_view(), name="event-sign-up"), #user, log
    path('cancel-sign-up-event/',views.CancelSignUpEventAPIView.as_view()),  #user, log
    path('profile/',views.GetProfileDetailsAPIView.as_view(), name="get-profile"),     #user|org, don't log  
    path('search-events/', views.SearchEvents.as_view(), name="serach-events"), #maybe log, check sql
    path('test',views.TestAPI.as_view()), #frontend validating user to backend, don't log
    path('get-all-events/', views.GetAllEvent.as_view(), name='get_all_events'), #ignore
    path('get-event/<str:eid>',views.GetEvent.as_view(), name='get-event'), #same as line 9, don't log
    path('auth-login/', views.Login.as_view(), name='login'), #log
    path('csrf/', views.csrf, name='get-csrf'), #log
    path('get-all-events/', views.GetAllEvent.as_view(), name='get-all-events'), #ignore
    path('auth-login/', views.Login.as_view(), name='get-all-events'), #should remove
    path('auth-verify-OTP/', views.VerifyOtp.as_view(), name='verify-OTP'), #verify success/fail, log
    path('auth-get-OTP/', views.GetOTP.as_view(), name='get-OTP'), #don't log
    path('auth-logout/', views.Logout.as_view(), name='logout'), #log
]

