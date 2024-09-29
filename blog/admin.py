from django.contrib import admin
from .models import Blog, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe

from django import forms


class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Blog
        fields = '__all__'


class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    prepopulated_fields = {'slug': ('title',)}  # title ustuni ga yozilsa sulg ga avtamatik ravishda yoziladi
    list_display = ('id', 'title', 'time_created', 'get_html_photo', 'is_published')   # adminkada shu columnlar kurinib turadi
    list_display_links = ('id', 'title')      #adminkadagi shu kolumnlarda ichkariga kirishga link bor
    search_fields = ('title', 'content')     # qidiruv tizimini ulash
    list_editable = ('is_published', )
    list_filter = ('is_published', 'time_created')  # filetr tizimini ishga tushiradi
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo_inner', 'is_published', 'time_created', 'time_update')
    readonly_fields = ('get_html_photo_inner', 'time_created', 'time_update')
    save_on_top = True

    def get_html_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='70'> ")

    def get_html_photo_inner(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='250'> ")

    get_html_photo.short_description = 'Минатюра'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', )


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
