from django.db.models.signals import post_save
from django.dispatch import receiver

from app_customer.models import CustomerModel

from utils.functions import generate_random_number


@receiver(post_save, sender=CustomerModel)
def set_customer_code_handler(sender, instance, **kwargs):
    if kwargs["created"]:
        if instance.customer_code in [None, ""]:
            while True:
                instance.customer_code = str(generate_random_number())
                instance.save()
                break
