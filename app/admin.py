from django.contrib import admin

# Register your models here.
from app import models


admin.site.register(models.Question)
admin.site.register(models.Author)
admin.site.register(models.Tag)
admin.site.register(models.Answer)