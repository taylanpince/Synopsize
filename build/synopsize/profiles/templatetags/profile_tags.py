from django import template
from django.conf import settings

from profiles.forms import RegistrationLoginForm


register = template.Library()


@register.inclusion_tag("profiles/registration_login_form.html")
def registration_login_form(form=None):
    if form is None:
        form = RegistrationLoginForm()

    return {
        "form": form,
        "MEDIA_URL": settings.MEDIA_URL,
    }


@register.filter
def is_favorite(synopsis, user):
    """
    Checks whether the synopsis is a favorite for the given user
    """
    profile = user.get_profile()

    return (profile.favorites.filter(pk=synopsis.pk).count() == 1)
