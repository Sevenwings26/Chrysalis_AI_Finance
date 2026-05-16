from django.contrib import admin
from .models import LearningCategory, Video, UserVideoProgress
# Register your models here.


admin.site.register(LearningCategory)
admin.site.register(Video)
admin.site.register(UserVideoProgress)


