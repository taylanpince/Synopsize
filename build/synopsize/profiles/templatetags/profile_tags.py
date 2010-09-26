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
