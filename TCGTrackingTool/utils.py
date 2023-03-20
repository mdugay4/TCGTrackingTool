from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.six import text_type

class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestampl):
        return  (user.is_active+user.pk+timestamp)