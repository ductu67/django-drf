from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.staff import views

router = DefaultRouter()
router.register(r'staffs', views.StaffViewSet)
router.register(r'staffs-plans', views.StaffPlansViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
