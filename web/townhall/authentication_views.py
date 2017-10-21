from models import AppUser


class CustomUserAuth(object):

    # checks if username and password are correct
    def authenticate(self, username=None, password=None):
        try:
            user = AppUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except AppUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = AppUser.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except AppUser.DoesNotExist:
            return None
