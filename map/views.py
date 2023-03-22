from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.models import User
from .models import Post, Comment
from users.models import House
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from .forms import CommentForm
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.shortcuts import redirect


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
    
class UserPostListView(ListView):
    model = Post
    template_name = 'map/user_posts.html'  
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDisplay(DetailView):
    model = Post
    template_name = 'map/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()
        context['post'] = post
        context['comments'] = comments
        context['form'] = CommentForm()
        return context
        
class PostComment(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm
    template_name = 'map/post_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PostComment, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse('post-detail', kwargs={'pk': post.pk})
        
class PostDetailView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        view = PostDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostComment.as_view()
        return view(request, *args, **kwargs)
    
 
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
    
class HouseCreateView(LoginRequiredMixin, CreateView):
    model = House
    fields = ['address', 'location', 'residents', 'description', 'image'] 
    template_name = "users/new_house_form.html"
    def form_valid(self, form):
        form.instance.owner = self.request.user
        print(form.errors)
        return super().form_valid(form)
    
class HouseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = House
    fields = ['residents', 'description', 'image']
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
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