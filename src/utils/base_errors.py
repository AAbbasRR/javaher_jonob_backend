from django.utils.translation import gettext as _


class BaseErrors:
    @classmethod
    def change_error_variable(cls, error_name, **kwargs):
        message = getattr(cls, error_name)
        for key, value in kwargs.items():
            message = message.replace("{%s}" % key, str(value))
        return message

    @classmethod
    def return_error_with_name(cls, error_name):
        return getattr(cls, error_name)

    # project
    url_not_found = _("URL Not Found.")
    server_error = _("Server Error.")

    # public sign up, login, forget pass, change pass
    passwords_do_not_match = _("Passwords do not match.")
    invalid_username_or_password = _("Invalid Username Or Password.")
    user_account_not_active = _("User Account Not Active.")
    old_password_is_incorrect = _("Old Password Is Incorrect")

    # global
    parameter_is_required = _("parameter {param_name} is required")
    object_not_found = _("{object} Not Found")
    invalid_field_value = _("Invalid Value")
