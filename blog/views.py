from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Post

from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

def home(request):
    return render(request, 'blog/home.html')

@login_required
def about(request):
    return render(request, 'blog/about.html')

def post_list(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().order_by('-created_at')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
            if not qs.exists():
                messages.warning(self.request, 'No se encontraron resultados.')
        else:
            if not qs.exists():
                messages.info(self.request, 'Aún no hay posts creados.')
        return qs


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'imagen']   
    template_name = 'blog/post_form.html'
    success_message = 'Post creado con éxito.'
    login_url = reverse_lazy('login')   
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'slug': self.object.slug})


class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'imagen']
    template_name = 'blog/post_form.html'
    success_message = 'Post actualizado.'
    login_url = reverse_lazy('login')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'slug': self.object.slug})


class PostDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    success_message = 'Post eliminado.'
    login_url = reverse_lazy('login')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('post_list')