from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from .models import News
from .serializers import NewsSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_permissions(self):
        """
        Returns the appropriate permissions based on the method or action.
        """
        if self.action == 'list':
            return [IsAuthenticated()]  # Anyone can view Newss
        elif self.action == 'create':
            return [IsAdminUser()]  # Only authenticated users can create
        elif self.action == 'destroy':
            return [IsAdminUser()]  # Only authenticated users can soft delete
        elif self.action == 'hard_delete':
            return [IsAdminUser()]  # Only authenticated users can hard delete
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        Handles listing all Newss.
        """
        queryset = News.active_objects.all()  # Use the custom manager to exclude soft-deleted items
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Handles soft deletion of an News.
        """
        instance = self.get_object()
        instance.Is_Delete = True  # Perform soft deletion
        instance.save()
        return Response({"message": "News soft-deleted successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def hard_delete(self, request, pk=None):
        """
        Handles hard deletion of an News.
        """
        instance = self.get_object()
        instance.delete()
        return Response({"message": "News hard-deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class TestRchnews(APIView):
    permission_classes = [AllowAny]  # ✅ Open access for testing
    def get(self, request):
        return Response({"message": "This is a test endpoint for the RchNews app."},status=status.HTTP_200_OK)