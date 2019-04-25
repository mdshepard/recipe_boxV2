from django.db import models

# The built-in User model already has secure handling for things like
# username, password, email address, and so on.
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField("Brief bio about the author")
    favorites = models.ManyToManyField(
        'Recipe', related_name='favorites', blank=True
        )

    def __str__(self):
        return self.user.username


class Recipe(models.Model):
    title = models.CharField("Title of recipe", max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.CharField("Description of the recipe", max_length=50)
    time_required = models.IntegerField("Time Required to make recipe")
    instructions = models.TextField("Recipe instructions")

    def __str__(self):
        return self.title

