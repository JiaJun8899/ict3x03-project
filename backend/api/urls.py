from django.urls import path
from . import views

urlpatterns = [
    # Organisers
    path("get-event-byorg/",views.EventsByOrganizationAPI.as_view(),name="get-event-org",),
    path("get-single-event/<str:event_id>",views.EventSingleByOrganizationAPI.as_view(),name="get-single-event",),
    path("register", views.RegisterUserAPIView.as_view(), name="register"),
    path("view-participants/<str:event_id>", views.EventParticipantAPI.as_view(), name="get-participants"),
    # Normal Users
    path('get-all-events/', views.EventAPI.as_view(), name='get-all-events'),
    path('update-user-details/',views.UpdateUserAPIView.as_view(), name="update-user-details"),
    path('sign-up-event/',views.SignUpEventAPIView.as_view(), name="event-sign-up"),
    path('cancel-sign-up-event/',views.CancelSignUpEventAPIView.as_view(),name='cancel-sign-up-event'),  
    path('profile/',views.GetProfileDetailsAPIView.as_view(), name="profile"),       
    path('search-events/', views.SearchEvents.as_view(), name="serach-events"),
    path('get-event/<str:eid>',views.GetEvent.as_view(),name="get-event"),
    path('get-past-events/',views.GetPastEventsByParticipant.as_view(), name="get-past-events"),
    path('get-upcoming-events/',views.GetUpcomingEventsByParticipant.as_view(),name="get-upcoming-events"),
    #Authentication
    path("auth-login/", views.Login.as_view(), name="auth-login"),
    path("check-auth", views.CheckAuth.as_view(), name="check-auth"),
    path("check-valid-organizer/<str:eid>", views.CheckValidEventOrg.as_view(), name="check-org-event"),
    path("auth-verify-OTP/", views.VerifyOtp.as_view(), name="auth-verify-OTP"),
    path("auth-get-OTP/", views.GetOTP.as_view(), name="auth-get-OTP"),
    path("auth-logout/", views.Logout.as_view(), name="auth-logout"),
    path("auth-reset-password/",views.ResetPassword.as_view(),name="auth-reset-password"),
    path("auth-change-password/",views.ChangePassword.as_view(),name="auth-change-password")
]
