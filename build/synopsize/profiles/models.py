from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    """
    Stores additional info for a registered user
    """
    user = models.ForeignKey(User, verbose_name=_("User"), unique=True, related_name="profiles")

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __unicode__(self):
        return self.user.email

    def name(self):
        """
        Returns a name for the user, depending on available info
        """
        if self.user.first_name and self.user.last_name:
            return u"%(first_name)s %(last_name)s" % {
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
            }
        elif self.user.first_name:
            return self.user.first_name
        else:
            return self.user.email
