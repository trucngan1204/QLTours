from django.contrib import admin
from django import forms
from django.utils.html import mark_safe
from .models import Staff, Tour, Blog, Category, Comment, Tag, User, Bill
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'avatar', 'is_staff']
    search_fields = ['username']
    readonly_fields = ['avatar']

    def avatar(self, user):
        return mark_safe("<img src='/static/{img_url}' alt='{alt}' width=120px />"
                         .format(img_url=user.image.name, alt=user.username))


class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'avatar', 'active']
    search_fields = ['name']

    def avatar(self, staff):
        return mark_safe("<img src='/static/{img_url}' alt='{alt}' width=120px />"
                         .format(img_url=staff.image.name, alt=staff.name))


class TourForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Tour
        fields = '__all__'


class TourAdmin(admin.ModelAdmin):
    form = TourForm
    list_display = ["id", "title", "avatar", "active"]
    search_fields = ['title', 'created_date', 'category__name']
    list_filter = ['title', 'category__name']
    readonly_fields = ['avatar']

    def avatar(self, tour): #hien hinh len server chi de doc khong sua chua
        return mark_safe("<img src='/static/{img_url}' alt='{alt}' width=120px />"
                         .format(img_url=tour.image.name, alt=tour.title))


class BlogForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Blog
        fields = '__all__'


class BlogAdmin(admin.ModelAdmin):
    form = BlogForm
    list_display = ['id', 'title', 'avatar', 'active']
    search_fields = ['title', 'created_date']
    readonly_fields = ['avatar']

    def avatar(self, blog):
        return mark_safe("<img src='/static/{img_url}' alt='{alt}' width=120px />"
                         .format(img_url=blog.image.name, alt=blog.title))


class CategoryAdmin(admin.ModelAdmin):
    # list_display = ['id', 'active']
    search_fields = ['name']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'blog', 'tour', 'description']
    search_fields = ['author']


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active']
    search_fields = ['name']


class BillAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'tour', 'total_price']
    search_fields = ['name']

# class ToursAppAdminSite(admin.AdminSite):
#     site.header = 'HỆ THỐNG QUẢN LÝ TOUR DU LỊCH'
#
#
# admin_site = ToursAppAdminSite('mytours')


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Tour, TourAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Bill, BillAdmin)