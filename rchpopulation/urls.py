from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PopulationViewSet

router = DefaultRouter()
router.register(r'population', PopulationViewSet, basename='population')

urlpatterns = [
    path('', include(router.urls)),
]