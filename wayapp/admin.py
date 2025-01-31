from django.contrib import admin
from .models import JobPost, JobDescription

# Register your models here.
#admin.site.register(UserProfile)
admin.site.register(JobPost)
admin.site.register(JobDescription)

