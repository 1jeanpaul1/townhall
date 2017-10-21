# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Interest
from .models import Permission
from .models import Role
from .models import AppUser
from .models import Category
from .models import UserPost
from .models import Comment


admin.site.register(Interest)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(AppUser)
admin.site.register(Category)
admin.site.register(UserPost)
admin.site.register(Comment)
