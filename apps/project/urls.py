
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.project import views

router = DefaultRouter()

router.register(r'projects-plans', views.ProjectsPlansViewSet)
router.register(r'projects', views.ProjectsViewSet)


urlpatterns = [
    path('', include(router.urls)),
]