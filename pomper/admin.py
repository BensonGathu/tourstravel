# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
# from .forms import *
from .models import *


# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Admin_User)
admin.site.register(Road_trips)
admin.site.register(Group_tours)
admin.site.register(Adventures_safaris)
admin.site.register(Gallery)
