from requests import Response
from rest_framework import viewsets
from .models import Event
from .serializers import EventSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class TestRchEven(APIView):
    permission_classes = [AllowAny]  # ✅ Open access for testing
    def get(self, request):
        return Response({"message": "This is a test endpoint for the RchData app."},status=status.HTTP_200_OK)
