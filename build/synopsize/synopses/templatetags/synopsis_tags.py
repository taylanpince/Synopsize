from django import template
from django.conf import settings

from synopses.forms import RatingForm


register = template.Library()


@register.inclusion_tag("synopses/rating_form.html")
def rating_form(synopsis):
    form = RatingForm()

    return {
        "form": form,
        "synopsis": synopsis,
        "MEDIA_URL": settings.MEDIA_URL,
    }
