from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from profiles.models import UserProfile


ACTION_LOGIN = 0
ACTION_REGISTER = 1
ACTION_CHOICES = (
    (ACTION_LOGIN, _("Login")),
    (ACTION_REGISTER, _("Register")),
)


class RegistrationLoginForm(forms.Form):
    """
    Base authentication form used in both login and registration
    """
    email = forms.EmailField(label=_("Your Email"), max_length=75)
    password = forms.CharField(label=_("Your Password"), widget=forms.PasswordInput)
    action = forms.ChoiceField(label=_("Action"), choices=ACTION_CHOICES, widget=forms.RadioSelect, initial=ACTION_LOGIN)

    def __init__(self, *args, **kwargs):
        self.user = None

        super(RegistrationLoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        if int(self.cleaned_data.get("action")) == ACTION_REGISTER:
            if self.cleaned_data.get("email", None):
                try:
                    user = User.objects.get(email__iexact=self.cleaned_data.get("email"))
                except User.DoesNotExist:
                    self.register()
                    self.user = self.login()

                    return self.cleaned_data

                raise forms.ValidationError(_(u"A user with this email already exists."))
        else:
            self.user = self.login()

            if self.user is None:
                raise forms.ValidationError(_(u"Please enter a correct email and password."))
            else:
                return self.cleaned_data

        return self.cleaned_data

    def login(self):
        """
        Authenticates the user
        """
        return authenticate(username=self.cleaned_data.get("email"), password=self.cleaned_data.get("password"))

    def register(self):
        """
        Registers a new user, with a generated username
        """
        username = self.cleaned_data.get("email").split("@", 1)[0]
        username_count = User.objects.filter(username__istartswith=username).count()

        if username_count > 0:
            username = "%(username)s-%(count)s" % {
                "username": username,
                "count": username_count,
            }

        user = User.objects.create_user(username, self.cleaned_data.get("email"), self.cleaned_data.get("password"))

        if not user:
            raise forms.ValidationError(_(u"There was an error trying to register."))

        if not user.check_password(self.cleaned_data.get("password")):
            user.set_password(self.cleaned_data.get("password"))
            user.save()

        return user


class UserForm(forms.ModelForm):
    """
    A form for editing User details
    """
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", )

    def clean(self):
        if self.instance.email != self.cleaned_data.get("email"):
            try:
                user = User.objects.get(email__iexact=self.cleaned_data.get("email"))
            except User.DoesNotExist:
                return self.cleaned_data

            raise forms.ValidationError(_(u"A user with this email already exists."))
        else:
            return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    """
    A form for editing UserProfile details
    """
    class Meta:
        model = UserProfile
