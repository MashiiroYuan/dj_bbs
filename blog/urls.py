"""mysites URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .feeds import LatestPostFeed
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/',views.post_list,name='post_list_by_tag'),
    # path('', views.PostListView.as_view, name='post_list'),
    path("<int:year>/<int:month>/<int:day>/<slug:post>/", views.post_detail, name="post_detail"),

    path('<int:post_id>/share/', views.post_share, name='post_share'),
    # path('email/',views.sendemail,name='email')
    path('feed/',LatestPostFeed(),name='post_feed'),
    path('search/',views.post_search,name='post_search'),

]
