from django.urls import path
from . import views

urlpatterns =[
    path('get-all-events/', views.EventAPI.as_view(), name='get-all-events'),
    path('get-event-byorg/', views.EventsByOrganizationAPI.as_view(), name='get-event-org'),
    path('get-single-event/<str:event_id>', views.EventSingleByOrganizationAPI.as_view(), name='get-single-event'),
    path('register',views.RegisterUserAPIView.as_view(), name="register"),
    path('view-participants/<str:event_id>', views.EventParticipantAPI.as_view()),
    # Normal Users
    path('update-user-details/',views.UpdateUserAPIView.as_view(), name="update-user-details"),
    path('sign-up-event/',views.SignUpEventAPIView.as_view(), name="event-sign-up"),
    path('cancel-sign-up-event/',views.CancelSignUpEventAPIView.as_view()),  
    path('profile/',views.GetProfileDetailsAPIView.as_view(), name="get-profile"),       
    path('search-events/', views.SearchEvents.as_view(), name="serach-events"),
    path('get-all-events/', views.GetAllEvent.as_view(), name='get_all_events'),
    path('csrf/', views.csrf),
    path('get-all-events/', views.GetAllEvent.as_view(), name='get_all_events'),
    path('check-auth', views.TestAPI.as_view()),
    path('check-valid-organizer/<str:eid>',views.validEventOrg),
    path('auth-login/', views.Login.as_view(), name='auth-login'),
    path('auth-verify-OTP/', views.VerifyOtp.as_view(), name='auth-verify-OTP'),
    path('auth-get-OTP/', views.GetOTP.as_view(), name='auth-get-OTP'),
    path('auth-logout/', views.Logout.as_view(), name='auth-logout'),
    path('auth-reset-password/', views.ResetPassword.as_view(), name='auth-reset-password'),
    path('auth-change-password/',views.ChangePassword.as_view(), name='auth-change-password'),
    path('csrf/', views.csrf),
]
