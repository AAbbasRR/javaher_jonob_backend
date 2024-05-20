from django.contrib.auth.models import AbstractUser, BaseUserManager, update_last_login
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.core.management import settings

from rest_framework_simplejwt.tokens import RefreshToken

from app_store.models import StoreModel

from utils.exceptions.core import InvalidUsernameOrPasswordError


class UserManager(BaseUserManager):
    def authenticate_user(self, username, password, **kwargs):
        try:
            user_obj = self.get(username=username, **kwargs)
            if user_obj.check_password(password):
                return user_obj
            else:
                raise InvalidUsernameOrPasswordError()
        except self.model.DoesNotExist:
            raise InvalidUsernameOrPasswordError()

    def create_user(self, username, password=None, **kwargs):
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, password):
        user = self.model(
            email=username,
        )
        user.set_password(password)
        user.type = User.UserTypeOptions.Staff
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.type = User.UserTypeOptions.Superuser
        user.is_active = True
        user.save(using=self._db)
        stores = StoreModel.objects.all()
        for store in stores:
            user.stores.add(store)
        return user

    def register_user(self, username, password=None, **kwargs):
        with transaction.atomic():
            user = self.create_user(username, password, **kwargs)
        return user


class User(AbstractUser):
    class UserTypeOptions(models.TextChoices):
        Superuser = "superuser", _("Superuser")
        Staff = "staff", _("Staff")
        Secretary = "secretary", _("Secretary")
        Worker = "worker", _("Worker")

    email = None
    is_superuser = None
    is_staff = None
    type = models.CharField(
        max_length=9,
        choices=UserTypeOptions.choices,
        default=UserTypeOptions.Worker,
        verbose_name=_("Type"),
    )
    stores = models.ManyToManyField(
        StoreModel,
        blank=True,
        related_name="store_users",
        verbose_name=_("Stores"),
    )

    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f"{self.pk} {self.username}"

    def formatted_last_login(self):
        if self.last_login is None:
            return None
        return self.last_login.strftime(
            f"{settings.DATE_INPUT_FORMATS} {settings.TIME_INPUT_FORMATS}"
        )

    def formatted_date_joined(self):
        return self.date_joined.strftime(
            f"{settings.DATE_INPUT_FORMATS} {settings.TIME_INPUT_FORMATS}"
        )

    def set_last_login(self):
        """
        :return: When the public logs in, we record her login time as the last login time
        """
        update_last_login(None, self)
        return self

    def create_new_token(self):
        """
        create new token for public object with jwt
        return:{
            refresh: jwt refresh token,
            access: jwt access token with 5 minute time life
        }
        """
        refresh_token = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh_token),
            "access": str(refresh_token.access_token),
        }

    def user_info(self, user_type="User"):
        return {
            "username": self.username,
            "date_joined": self.formatted_date_joined(),
            "last_login": self.formatted_last_login(),
            "full_name": self.get_full_name(),
            "type": self.type,
        }

    def user_login_detail(self):
        user_info = self.user_info()
        user_info.update(
            {
                "token": self.create_new_token(),
            }
        )
        return user_info
