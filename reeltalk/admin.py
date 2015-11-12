from __future__ import unicode_literals

from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from .models import (
    Show,
    Review,
    User,
    Group
)

classes = [Show, Review, Group]


class ModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser or True:
            messages.error(request, "Only superusers can change models")
            return False
        return super(ModelAdmin, self).save_model(request, obj, form, change)

for c in classes:
    admin.site.register(c, ModelAdmin)
