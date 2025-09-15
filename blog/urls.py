from django.urls import path
from . import views
from .views import (
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView,
)

urlpatterns = [
    path('', views.home, name='home'),                   
    path('about/', views.about, name='about'),           
    
    
    path('blog/', views.post_list, name='post_list'),
    path('blog/<slug:slug>/', views.post_detail, name='post_detail'),

   
    path('posts/', PostListView.as_view(), name='post_list_cbv'),
    path('posts/nuevo/', PostCreateView.as_view(), name='post_create'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post_detail_cbv'),
    path('posts/<slug:slug>/editar/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<slug:slug>/borrar/', PostDeleteView.as_view(), name='post_delete'),
]
