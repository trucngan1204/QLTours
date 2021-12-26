from django.urls import path, include
from . import views
# from .admin import admin.site
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('tours', views.TourViewSet)
router.register('blogs', views.BlogViewSet)
router.register('categories', views.CategoryViewSet)
router.register('staffs', views.StaffViewSet)
router.register('tags', views.TagViewSet)
router.register('users', views.UserViewSet)
router.register('comments', views.CommentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('admin/', admin.site.urls),
    path('oauth2-info/', views.AuthInfo.as_view())
]

