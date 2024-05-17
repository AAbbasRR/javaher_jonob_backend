from django.db.models.signals import post_save
from django.dispatch import receiver

from app_factor.models import FactorItemsModel


@receiver(post_save, sender=FactorItemsModel)
def set_factor_item_price_tax_handler(sender, instance, **kwargs):
    if kwargs["created"]:
        if instance.price is None:
            instance.price = instance.product.price
        if instance.tax is None:
            instance.tax = instance.product.tax
        instance.save()
        if (
            instance.price != instance.product.price
            or instance.tax != instance.product.tax
        ):
            instance.factor.is_accepted = False
            instance.factor.save()
