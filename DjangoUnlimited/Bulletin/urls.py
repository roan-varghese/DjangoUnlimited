from django.urls import path
from . import views
from .views import BulletinView, EditBulletin, PostDetailView,CreatePostView

urlpatterns = [
    path('bulletin/', BulletinView.as_view(), name='bulletin'),
    path('post/new/', CreatePostView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', EditBulletin.as_view(), name='post_edit'),
    path('post/<int:pk>/', PostDetailView, name='post_detail'),
    path('allPosts', views.AllPosts, name='all_posts')

]