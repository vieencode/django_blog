from django.urls import path
from . import views
from .feeds import LatestPostFeed

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name = 'post_detail'),
    path('draft/<slug:post>/',
         views.post_detail_draft,
         name = 'post_detail'),
    path("about/", views.blog_about, name="blog_about"),
    path("tech_specs/", views.blog_tech_specs, name="blog_tech_specs"),
    path('feed/', LatestPostFeed(), name='post_feed'),
    path('like/', views.post_like, name='like'), 
]