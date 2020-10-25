
from django.views.generic import TemplateView
from django.urls import path, include
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from accounts import urls as accounts_urls
from django.contrib import admin

# email varification
from . import views as account_view
from accounts.views import SignUpView,  ProfileView, ActivateAccount

# app_name = 'accounts'

urlpatterns = [

    path('signup/', SignUpView.as_view(), name='signup'),
    path('update/profile/<int:pk>/', ProfileView.as_view(), name='update_profile'),

    # login and logout views
    # path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    # oauth/ Social login urls [this is for project.urls]
    # path('accounts/', include('allauth.urls')),
    # path('oauth/', include('social_django.urls', namespace='social')),  # <-- here

    path('social/login/', account_view.SocialLoginView.as_view(), name='social_complete'),
    path('user/set/password/', account_view.set_user_password, name='set_password'),

    # profile Page
    path('profile/<pk>/', TemplateView.as_view(template_name='accounts/profile.html'), name='profile'),

    # other urls
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),

    # Change Password
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/change-password.html',
            success_url = '/'
        ),
        name='change_password'
    ),

    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password/password-reset/password_reset.html',
             subject_template_name='password/password-reset/password_reset_subject.txt',
             email_template_name='password/password-reset/password_reset_email.html',
             #success_url='/login/'
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
            # logout(request),
            template_name='password/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
