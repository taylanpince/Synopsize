from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.forms.models import inlineformset_factory, modelformset_factory
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from djangoratings.views import AddRatingView

from synopses.forms import SynopsisForm, PointForm, FactForm, ValidatingFormSet, RatingForm
from synopses.models import Synopsis, Fact, Point


def list_synopsis(request):
    """
    List all recent synopses
    """
    synopses = Synopsis.objects.order_by("-created")[:10]

    return render_to_response("synopses/list_synopsis.html", {
        "synopses": synopses,
    }, context_instance=RequestContext(request))


def detail_synopsis(request, synopsis_id):
    """
    Detail page for a specific synopsis
    """
    synopsis = get_object_or_404(Synopsis, pk=synopsis_id)

    return render_to_response("synopses/detail_synopsis.html", {
        "synopsis": synopsis,
    }, context_instance=RequestContext(request))


def search_synopsis(request):
    """
    Display search results for given keywords
    """
    pass


def create_synopsis(request):
    """
    Create a new synopsis
    """
    FactFormset = inlineformset_factory(Synopsis, Fact, formset=ValidatingFormSet, exclude=["order"], extra=3, can_delete=False)
    PointFormset = inlineformset_factory(Synopsis, Point, formset=ValidatingFormSet, exclude=["order"], extra=3, can_delete=False)

    if request.method == "POST":
        form = SynopsisForm(request.POST)

        if form.is_valid():
            synopsis = form.save(commit=False)
            synopsis.user = request.user

            fact_formset = FactFormset(request.POST, instance=synopsis, prefix="facts")
            point_formset = PointFormset(request.POST, instance=synopsis, prefix="points")

            if fact_formset.is_valid() and point_formset.is_valid():
                synopsis.save()

                facts = fact_formset.save()
                points = point_formset.save()

                return HttpResponseRedirect(synopsis.get_absolute_url())
        else:
            synopsis = Synopsis()
            fact_formset = FactFormset(request.POST, instance=synopsis, prefix="facts")
            point_formset = PointFormset(request.POST, instance=synopsis, prefix="points")
    else:
        form = SynopsisForm()
        synopsis = Synopsis()
        fact_formset = FactFormset(instance=synopsis, prefix="facts")
        point_formset = PointFormset(instance=synopsis, prefix="points")

    return render_to_response("synopses/create_synopsis.html", {
        "form": form,
        "fact_formset": fact_formset,
        "point_formset": point_formset,
    }, context_instance=RequestContext(request))


def update_synopsis(request, synopsis_id):
    """
    Update a specific synopsis
    """
    synopsis = get_object_or_404(Synopsis, pk=synopsis_id)

    if not (synopsis.user == request.user):
        raise Http404

    FactFormset = inlineformset_factory(Synopsis, Fact, formset=ValidatingFormSet, exclude=["order"], extra=3)
    PointFormset = inlineformset_factory(Synopsis, Point, formset=ValidatingFormSet, exclude=["order"], extra=3)

    if request.method == "POST":
        form = SynopsisForm(request.POST, instance=synopsis)

        if form.is_valid():
            synopsis = form.save(commit=False)
            synopsis.user = request.user

            fact_formset = FactFormset(request.POST, instance=synopsis, prefix="facts")
            point_formset = PointFormset(request.POST, instance=synopsis, prefix="points")

            if fact_formset.is_valid() and point_formset.is_valid():
                synopsis.save()

                facts = fact_formset.save()
                points = point_formset.save()

                return HttpResponseRedirect(synopsis.get_absolute_url())
        else:
            fact_formset = FactFormset(request.POST, instance=synopsis, prefix="facts")
            point_formset = PointFormset(request.POST, instance=synopsis, prefix="points")
    else:
        form = SynopsisForm(instance=synopsis)
        fact_formset = FactFormset(instance=synopsis, prefix="facts")
        point_formset = PointFormset(instance=synopsis, prefix="points")

    return render_to_response("synopses/update_synopsis.html", {
        "form": form,
        "synopsis": synopsis,
        "fact_formset": fact_formset,
        "point_formset": point_formset,
    }, context_instance=RequestContext(request))


@login_required
def delete_synopsis(request, synopsis_id):
    """
    Delete a specific synopsis
    """
    synopsis = get_object_or_404(Synopsis, pk=synopsis_id)

    if request.GET.get("confirm", False):
        synopsis.delete()
        synopsis = None

    return render_to_response("synopses/delete_synopsis.html", {
        "synopsis": synopsis,
    }, context_instance=RequestContext(request))


@login_required
def rate_synopsis(request, synopsis_id):
    """
    Rate a specific synopsis
    """
    synopsis = get_object_or_404(Synopsis, pk=synopsis_id)

    if request.method == "POST":
        form = RatingForm(request.POST)

        if form.is_valid():
            content_type = ContentType.objects.get_for_model(synopsis)
            response = AddRatingView()(request, **{
                "content_type_id": content_type.pk,
                "object_id": synopsis.pk,
                "field_name": "rating",
                "score": form.cleaned_data.get("rating"),
            })

            if response.status_code == 200:
                return HttpResponseRedirect(synopsis.get_absolute_url())
            else:
                print response.content
    else:
        form = RatingForm()

    return render_to_response("synopses/rate_synopsis.html", {
        "synopsis": synopsis,
        "form": form,
    }, context_instance=RequestContext(request))
