from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Event
from .serializers import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]  # Change to AllowAny if you want public access

class EventQueryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        hn = request.data.get('HN')
        hn_year = request.data.get('HnYear')

        if not hn or not hn_year:
            return Response({"error": "HN and HnYear are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Event.objects.get(HN=hn, HnYear=hn_year)
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)


class TestRchEven(APIView):
    permission_classes = [AllowAny]  
    def get(self, request):
        return Response({"message": "This is a test endpoint for the RchData app."},status=status.HTTP_200_OK)
