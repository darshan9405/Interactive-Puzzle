from django.contrib import admin

# Register your models here.
from .models import user, question

admin.site.register(user)
admin.site.register(question)
