from django.shortcuts import render
from .models import Post, Dwelling

# Create your views here.
def home(request):
    context = {
        'posts' : Post.objects.all(),
        'dwellings' : Dwelling.objects.all()
    }
    return render(request, "map/Home.html", context)
    
def feed(request):
    return render(request, 'map/feed.html')