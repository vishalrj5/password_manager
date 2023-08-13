from django.db import models
from cryptography.fernet import Fernet

from apps.users.models import AbstractDateFieldMix, Users
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password

# Create your models here.
class UserPasswords(AbstractDateFieldMix):
    user                    = models.ForeignKey(Users, related_name='users', on_delete=models.CASCADE)
    password                = models.CharField(_('unhashed_password'), max_length=500, blank = True, null = True)
    raw_password            = models.TextField(_('hashed_password'), max_length=500, blank = True, null = True)
    expiry                  = models.CharField(_('expiry'), max_length=100, blank = True, null = True)
    
    view_users             = models.ManyToManyField(
        Users,
        verbose_name        = _("view_users"),
        blank               = True,
        help_text           = _(
            "These users can view passwords"
        ),
        related_name        = "view_users",
        related_query_name  = "view_users",
    
    )
    
    edit_users             = models.ManyToManyField(
        Users,
        verbose_name        = _("edit_users"),
        blank               = True,
        help_text           = _(
            "These users can view passwords"
        ),
        related_name        = "edit_users",
        related_query_name  = "edit_users",
    
    )
