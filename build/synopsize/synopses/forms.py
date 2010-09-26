from django import forms
from django.utils.translation import ugettext_lazy as _

from synopses.models import Synopsis, Point, Fact, Journal


class SynopsisForm(forms.ModelForm):
    """
    A Synopsis form
    """
    journal_name = forms.CharField(label=_("Journal Name"), required=False)

    class Meta:
        model = Synopsis
        exclude = ("user",)

    def save(self, *args, **kwargs):
        obj = super(SynopsisForm, self).save(*args, **kwargs)

        if not obj.journal and self.cleaned_data.get("journal_name", None):
            journal = Journal(name=self.cleaned_data.get("journal_name"))
            journal.save()

            obj.journal = journal

            if kwargs.get("commit", True):
                obj.save()

        return obj


class PointForm(forms.ModelForm):
    """
    A Point form
    """
    class Meta:
        model = Point
        exclude = ("order", "synopsis")


class FactForm(forms.ModelForm):
    """
    A Fact form
    """
    class Meta:
        model = Fact
        exclude = ("order", "synopsis")


class ValidatingFormSet(forms.models.BaseModelFormSet):
    """
    A FormSet that makes sure there is at least one object in it
    """
    def clean(self):
        cleaned_data = super(ValidatingFormSet, self).clean()

        if cleaned_data:
            has_object = False

            for form in self.forms:
                if form.has_changed():
                    has_object = True

            if not has_object:
                raise forms.ValidationError(_(u"You have to enter at least one point and one fact."))

            return cleaned_data
