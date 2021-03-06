from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.validators import email_re


class EmailBackend(ModelBackend):
    """
    Uses email as the username for authentication
    """
    def authenticate(self, username=None, password=None):
        if email_re.search(username):
            try:
                user = User.objects.get(email=username)

                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None

        return None
