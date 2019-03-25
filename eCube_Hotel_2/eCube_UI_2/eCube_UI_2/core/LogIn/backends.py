from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class UserAuthenticationBackend(ModelBackend):
    """
    Authenticate against the LOGIN and PASSWORD.

    Use the login name and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(UserName=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
    
    def get_user(self, user_id):
        try:
            user = User.objects.get(User_ID=user_id)
        except Exception as e:
            return None
        return user