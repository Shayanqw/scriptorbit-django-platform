from django.contrib import admin
from .models import *


# Register your models here.

class ImageInlinesAdmin(admin.TabularInline):
    model = Images
    extra = 2


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create', 'update')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'file')
    inlines = [ImageInlinesAdmin]
    fieldsets = (
        (None, {
            'fields': ('meta_description', 'meta_keywords')
        }),
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'meta_description','meta_keywords')
        }),
    )


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'category', 'applied_at')
    list_filter = ('category', 'how_hear')
    readonly_fields = ('applied_at',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at','author')
    list_filter = ('created_at',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    # If using RichTextUploadingField, ensure static/js for CKEditor loads in admin automatically.
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Images)
