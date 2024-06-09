from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.core.management import settings


class AbstractDateQueryset(models.QuerySet):
    def delete(self):
        return self.update(is_deleted=True, deleted_at=timezone.now())


class AbstractDateManager(models.Manager):
    def get_queryset(self):
        return AbstractDateQueryset(self.model, self._db).filter(is_deleted=False)


class AbstractDateModel(models.Model):
    class Meta:
        abstract = True
        ordering = ["-create_at"]

    create_at = models.DateTimeField(verbose_name=_("Created Time"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated Time"), auto_now=True)
    is_deleted = models.BooleanField(
        editable=False, default=False, verbose_name=_("Is Deleted")
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True, editable=True, verbose_name=_("Deleted Time")
    )

    objects = AbstractDateManager()

    def formatted_create_at(self):
        return self.create_at.strftime(
            f"{settings.DATE_INPUT_FORMATS} {settings.TIME_INPUT_FORMATS}"
        )

    def formatted_updated_at(self):
        return self.updated_at.strftime(
            f"{settings.DATE_INPUT_FORMATS} {settings.TIME_INPUT_FORMATS}"
        )

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
