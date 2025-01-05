import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 6:
            raise ValidationError(
                _("Password must be at least 6 characters long."),
                code='password_too_short',
            )
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("Password must contain at least one uppercase letter."),
                code='password_no_upper',
            )
        if not any(char.islower() for char in password):
            raise ValidationError(
                _("Password must contain at least one lowercase letter."),
                code='password_no_lower',
            )
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                _("Password must contain at least one special character."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _(
            "Your password must be at least 6 characters long, contain at least one uppercase letter, "
            "one lowercase letter, and one special character."
        )

class CustomEmailValidator:
    def validate(self, email, user=None):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValidationError(
                _("Enter a valid email address."),
                code='invalid_email',
            )

    def get_help_text(self):
        return _("Your email address must be valid and in the correct format (e.g., user@example.com).")
