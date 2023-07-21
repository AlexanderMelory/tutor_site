from django.urls import path
from .views import index, contancts, services, \
    profile, ChangeUserInfoView, UserPasswordChangeView, \
    UserLoginView, UserLogoutView, RegisterUserView, RegisterDoneView, \
    user_activate, UserPasswordResetView, UserPasswordResetConfirmView

app_name = 'main'

urlpatterns = [
    path('accounts/reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('accounts/password/reset/', UserPasswordResetView.as_view(),
         name='password_reset'),
    path('tutor/register/done', RegisterDoneView.as_view(),
         name='register_done'),
    path('tutor/register', RegisterUserView.as_view(),
         name='register'),
    path('tutor/register/activate/<str:sign>/', user_activate,
         name='register_activate'),
    path('tutor/logout/', UserLogoutView.as_view(),
         name='logout'),
    path('tutor/login/', UserLoginView.as_view(),
         name='login'),
    path('tutor/profile/', profile,
         name='profile'),
    path('tutor/profile/change/', ChangeUserInfoView.as_view(),
         name='profile_change'),
    path('tutor/profie/password_change/', UserPasswordChangeView.as_view(),
         name='password_change'),
    path('tutor/services/', services,
         name='services'),
    path('tutor/contacts/', contancts,
         name='contacts'),
    path('', index,
         name='index')
]
