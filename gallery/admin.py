from django.contrib import admin
from .models import Video, Image, Category
from .models import Assignment
from .models import Ebook



admin.site.register(Video)
admin.site.register(Image)
admin.site.register(Category)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('instructor', 'created_at')




@admin.register(Ebook)
class EbookAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'upload_type', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('instructor', 'created_at', 'upload_type')