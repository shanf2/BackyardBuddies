from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from users.models import House
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

# Create your views here.
def home(request):
    context = {
        'houses' : serializers.serialize("json", House.objects.all(),cls=DjangoJSONEncoder)
    }
    return render(request, "map/Home.html", context)
    
    
class PostListView(ListView):
    model = Post
    template_name = 'map/feed.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 15
    
class PostDetailView(DetailView):
    model = Post
 
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False
            
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/feed'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False
       
def feed(request):
    return render(request, 'map/feed.html')
    
class HouseDetailView(DetailView):
    model = House
    
class HouseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = House
    fields = ['residents', 'description']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
    def test_func(self):
        House = self.get_object()
        if self.request.user == House.owner:
            return True
        else:
            return False
            
class HouseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = House
    success_url = '/feed'
    
    def test_func(self):
        House = self.get_object()
        if self.request.user == House.owner:
            return True
        else:
            return False