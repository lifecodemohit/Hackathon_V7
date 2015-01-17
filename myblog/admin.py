from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
# Register your models here.
from myblog.models import *
class CommentsInline(admin.StackedInline):
    model = Comment
    extra = 0    

class QuestionAdmin(admin.ModelAdmin):
    inlines = [CommentsInline]

admin.site.register(Question,QuestionAdmin)