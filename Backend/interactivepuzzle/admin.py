from django.contrib import admin

# Register your models here.
from .models import question,CustomUser,submissions,session

admin.site.register(question)

admin.site.register(CustomUser)

admin.site.register(submissions)

admin.site.register(session)