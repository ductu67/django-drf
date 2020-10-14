from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.authentication import views

router = DefaultRouter()
urlpatterns = [
    path("auth/", include(router.urls)),
    path("auth/login/", views.LoginViewSet.as_view()),
    path("auth/logout/", views.LogoutViewSet.as_view()),
]
