from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

#custom classes and modules
from accounts.forms import SignUpForm, ProfileForm
from accounts.tokens import account_activation_token


"""
############   account activation using email   ########
"""


# Sign Up View
class SignUpView(View):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('emails/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Please Confirm your email to complete registration.'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})


from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from accounts.tokens import account_activation_token
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.customer.email_confirmed = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, ('Your account have been confirmed.'))
            # return redirect('profile')
            return HttpResponseRedirect(reverse('profile',
                                kwargs={'pk':uid,}))
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('index')


from django.contrib.auth.mixins import LoginRequiredMixin

# Edit Profile View
class ProfileView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = User
    form_class = ProfileForm

    def get_success_url(self):
        pk = self.request.user.customer.id
        return reverse_lazy('profile', kwargs={
                              'pk':pk , })

    template_name = 'accounts/profile_update_form.html'


"""
############    Social Login section    ########
"""
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from social_django.models import UserSocialAuth


class SocialLoginView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user

        try:
            github_login = user.social_auth.get(provider='github')
        except UserSocialAuth.DoesNotExist:
            github_login = None

        try:
            twitter_login = user.social_auth.get(provider='twitter')
        except UserSocialAuth.DoesNotExist:
            twitter_login = None

        try:
            facebook_login = user.social_auth.get(provider='facebook')
        except UserSocialAuth.DoesNotExist:
            facebook_login = None

        from allauth.socialaccount.models import SocialAccount
        try:
            social_user = SocialAccount.objects.filter(provider='google', user_id=user.id)

            print('social_user 1: ', social_user)

            # print('google_login 1: ', google_login)
        except :
            social_user = None

        print('social_user 2: ', social_user)

        can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
        print(user.social_auth.count())

        if social_user and user.has_usable_password():
            can_disconnect_from_google = True
        else:
            can_disconnect_from_google = False

        return render(request, 'social_login/login_complete.html', {
            'social_user': social_user,
            'can_disconnect_from_google':can_disconnect_from_google,
            'github_login': github_login,
            'twitter_login': twitter_login,
            'facebook_login': facebook_login,
            'can_disconnect': can_disconnect
        })


@login_required
def set_user_password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'social_login/password.html', {'form': form})
