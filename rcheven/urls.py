from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventQueryView, EventViewSet, TestRchEven

router = DefaultRouter()
router.register(r'event', EventViewSet)

urlpatterns = [
    path('test/', TestRchEven.as_view(), name='test_event'),
    path('events/', EventQueryView.as_view(), name='event_query'),  # ✅ Changed
    path('', include(router.urls)),
]