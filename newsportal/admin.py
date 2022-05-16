from django.contrib import admin
from .models import Post, Category
from modeltranslation.admin import TranslationAdmin


class CategoryAdmin(TranslationAdmin):
    model = Category

class PostlAdmin(TranslationAdmin):
    model = Post

admin.site.register(Post)
admin.site.register(Category)

