from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from synopses.forms import SynopsisForm, PointForm, FactForm, ValidatingFormSet
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
    FactFormset = modelformset_factory(Fact, form=FactForm, formset=ValidatingFormSet, extra=3)
    PointFormset = modelformset_factory(Point, form=PointForm, formset=ValidatingFormSet, extra=3)

    if request.method == "POST":
        form = SynopsisForm(request.POST)
        fact_formset = FactFormset(request.POST)
        point_formset = PointFormset(request.POST)

        if form.is_valid() and fact_formset.is_valid() and point_formset.is_valid():
            synopsis = form.save(commit=False)
            synopsis.user = request.user
            synopsis.save()

            facts = fact_formset.save()
            points = point_formset.save()

            synopsis.facts.add(*facts)
            synopsis.points.add(*points)

            return HttpResponseRedirect(synopsis.get_absolute_url())
    else:
        form = SynopsisForm()
        fact_formset = FactFormset()
        point_formset = PointFormset()

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

    FactFormset = modelformset_factory(Fact, form=FactForm, formset=ValidatingFormSet, extra=3)
    PointFormset = modelformset_factory(Point, form=PointForm, formset=ValidatingFormSet, extra=3)

    if request.method == "POST":
        form = SynopsisForm(request.POST, instance=synopsis)
        fact_formset = FactFormset(request.POST, queryset=synopsis.facts.all())
        point_formset = PointFormset(request.POST, queryset=synopsis.points.all())

        if form.is_valid() and fact_formset.is_valid() and point_formset.is_valid():
            synopsis = form.save(commit=False)
            synopsis.user = request.user
            synopsis.save()

            facts = fact_formset.save()
            points = point_formset.save()

            synopsis.facts.add(*facts)
            synopsis.points.add(*points)

            return HttpResponseRedirect(synopsis.get_absolute_url())
    else:
        form = SynopsisForm(instance=synopsis)
        fact_formset = FactFormset(queryset=synopsis.facts.all())
        point_formset = PointFormset(queryset=synopsis.points.all())

    return render_to_response("synopses/update_synopsis.html", {
        "form": form,
        "fact_formset": fact_formset,
        "point_formset": point_formset,
    }, context_instance=RequestContext(request))


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
