"""recipebox URL Configuration

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
from django.conf.urls import url
from recipebox import views
from recipebox.models import *


admin.site.register(Author)
admin.site.register(Recipe)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.recipe_list, name="recipes"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_action, name="logout"),
    path("recipes/<int:recipe_id>", views.recipe_detail, name="recipe_detail"),
    path("author/<int:author_id>", views.author_detail, name="author_detail"),
    path("add/user/", views.useradd, name="signup"),
    path("add/author/", views.authoradd, name="authoradd"),
    path("add/recipe/", views.recipeadd, name="recipeadd"),
    path('profile/', views.profile, name='profile'),
    path('favorite/<int:recipe_id>', views.favorite, name='favorite'),
    path('update/', views.update_recipe, name='update'),
]
