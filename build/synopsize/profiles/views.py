from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout as auth_logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from profiles.forms import RegistrationLoginForm
from profiles.forms import UserForm, UserProfileForm
from profiles.models import UserProfile


def register_or_login(request):
    """
    Registers or logs a user in
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("profiles_profile_landing"))

    if request.method == "POST":
        form = RegistrationLoginForm(request.POST)

        if form.is_valid():
            login(request, form.user)
            
            if request.is_ajax():
                return render_to_response("profiles/registration_complete.html", {
                    
                }, context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect(request.GET.get("next", settings.LOGIN_REDIRECT_URL))
    else:
        form = RegistrationLoginForm()

    if request.is_ajax():
        template = "profiles/registration_login_form.html"
    else:
        template = "profiles/registration_login.html"

    return render_to_response(template, {
        "form": form,
        "next": request.GET.get("next", None),
    }, context_instance=RequestContext(request))


def logout(request):
    auth_logout(request)

    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)


@login_required
def profile_landing(request):
    """
    Redirects to profile page
    """
    return HttpResponseRedirect(reverse("profiles_profile", kwargs={
        "username": request.user.username,
    }))


def profile(request, username):
    """
    Profile detail page
    """
    user = get_object_or_404(User, username=username)

    return render_to_response("profiles/profile.html", {
        "profile_user": user,
    }, context_instance=RequestContext(request))


@login_required
def profile_edit(request):
    """
    Edit profile page
    """
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            return HttpResponseRedirect(reverse("profiles_profile_landing"))
    else:
        user_form = UserForm(instance=request.user)

    return render_to_response("profiles/profile_form.html", {
        "user_form": user_form,
    }, context_instance=RequestContext(request))
