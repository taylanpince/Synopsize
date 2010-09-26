from django.db import models
from django.utils.translation import ugettext_lazy as _

from djangoratings.fields import RatingField
from tagging.fields import TagField


class Synopsis(models.Model):
    """
    A class that encapsulates a single synopsis in the system
    """
    user = models.ForeignKey("auth.User", verbose_name=_("User"), related_name="synopses")
    title = models.CharField(_("Title"), max_length=255)
    journal = models.ForeignKey("Journal", verbose_name=_("Journal"), related_name="synopses", blank=True, null=True)
    url = models.URLField(_("URL"), verify_exists=True, blank=True, null=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified"), auto_now=True)
    rating = RatingField(range=5, can_change_vote=True)
    tags = TagField()

    class Meta:
        verbose_name = _("Synopsis")
        verbose_name_plural = _("Synopses")

    def __unicode__(self):
        return u"%(title)s by %(user)s" % {
            "title": self.title,
            "user": self.user.username,
        }


class Point(models.Model):
    """
    A point in a synopsis
    """
    synopsis = models.ForeignKey(Synopsis, verbose_name=_("Synopsis"), related_name="points")
    content = models.TextField(_("Content"))
    order = models.PositiveSmallIntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Point")
        verbose_name_plural = _("Points")
        ordering = ["order"]

    def __unicode__(self):
        return u"Point for %s" % self.synopsis.title


class Fact(models.Model):
    """
    A fact in a synopsis
    """
    synopsis = models.ForeignKey(Synopsis, verbose_name=_("Synopsis"), related_name="facts")
    content = models.TextField(_("Content"))
    order = models.PositiveSmallIntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Fact")
        verbose_name_plural = _("Facts")
        ordering = ["order"]

    def __unicode__(self):
        return u"Fact for %s" % self.synopsis.title


class Journal(models.Model):
    """
    A journal tied to several synopses
    """
    name = models.CharField(_("Name"), max_length=255)
    url = models.URLField(_("URL"), verify_exists=True, blank=True, null=True)

    class Meta:
        verbose_name = _("Journal")
        verbose_name_plural = _("Journals")

    def __unicode__(self):
        return self.name
