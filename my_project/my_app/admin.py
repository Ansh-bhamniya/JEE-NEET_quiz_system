from django.contrib import admin
from .models import Profile
from .models import Category
from .models import Quiz, Question , Choice 
# Register your models here.

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
