# grouping import
from rest_framework.validators import UniqueValidator

from django.core.validators import RegexValidator

from utils import BaseErrors

PhoneRegex = r"^{?(0?9[0-9]{9,9}}?)$"

PhoneNumberRegexValidator = RegexValidator(
    PhoneRegex, BaseErrors.invalid_mobile_number_format
)
