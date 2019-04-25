from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse, redirect  # noqa
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Author, Recipe
from .forms import *


def recipe_list(request):
    recipes = Recipe.objects.all
    return render(request, "recipe_list.html", {"recipes": recipes})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, "recipe_detail.html", {"recipe": recipe})


def author_detail(request, author_id):
    data = {}
    author = get_object_or_404(Author, pk=author_id)
    recipe = Recipe.objects.filter(author=author_id)
    data.update({'recipe': recipe, 'author': author})
    data.update(update_recipe(request, recipe))
    if request.method == 'POST':
        update_recipe(request, recipe)
        return HttpResponseRedirect(
            reverse('recipe', kwargs={"recipe_id": recipe_id})
            )
    return render(request, 'recipe.html', data)


def logout_action(request):
    html = "logout.html"
    logout(request)
    return redirect(request.GET.get("next", "/"))


def login_view(request):
    html = "login.html"
    form = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data["username"], password=data["password"]
            )
            if user is not None:
                login(request, user)
                return redirect(request.GET.get("next", "/"))
    else:
        form = LoginForm()
    return render(request, html, {"form": form})


@staff_member_required(login_url="/login/")
def useradd(request):
    html = "formadd.html"
    form = None

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            username = data["username"]
            raw_password = data["password1"]
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(request.GET.get("recipes/"))

    else:
        form = UserCreationForm()
    return render(request, "useradd.html", {"form": form})


@login_required
def authoradd(request):
    html = "authoradd.html"
    form = None

    if request.method == "POST":
        form = AuthorAddForm(request.POST, user=request.user)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(user=data["user"], bio=data["bio"])
            return render(request, "updated.html")
    else:
        form = AuthorAddForm(user=request.user)

    return render(request, html, {"form": form})


@login_required
def recipeadd(request):
    html = "recipeadd.html"
    form = None

    if request.method == "POST":
        form = RecipeAddForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data["title"],
                author=data["author"],
                description=data["description"],
                time_required=data["time_required"],
                instructions=data["instructions"],
            )
            return render(request, "updated.html")

    else:
        form = RecipeAddForm()

    return render(request, html, {"form": form})


@login_required()
def profile(request):
    if request.user.author:
        author = request.user.author
        recipes = Recipe.objects.filter(author_id=author)
        favorites = request.user.author.favorites.all()
    return render(request, 'profile.html', {'recipes':recipes, 'author': author, 'favorites':favorites})


def favorite(request, recipe_id):
    """to favorite a recipe"""
    user = request.user.author
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe not in user.favorites.all():
        user.favorites.add(recipe)
    elif recipe in user.favorites.all():
        user.favorites.remove(recipe)
    return HttpResponseRedirect(reverse('profile'))


def update_recipe(request, recipe):
    form = UpdateForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        recipe.title = data['title']
        recipe.description = data['description']
        recipe.instructions = data['instructions']
        recipe.time_requirex = data['time']
        recipe.save()
    return
