from django.shortcuts import render

# Create your views here.
def privacy(request):
    return render(request, 'privacy.html')
