from profiles.models import UserProfile


def create_user_profile(sender, instance, created, **kwargs):
    """
    A simple post_save signal tied to ``django.contrib.auth.User`` that 
    automatically creates a ``UserProfile`` linked to a new user.
    """
    if created:
        # Check to see if a profile with this user already exists
        # We have to do this just in case the signal gets fired twice
        # And catching IntegrityError is not properly supported yet
        try:
            UserProfile._default_manager.get(user=instance)
        except UserProfile.DoesNotExist:
            up = UserProfile(user=instance)
            up.save()
