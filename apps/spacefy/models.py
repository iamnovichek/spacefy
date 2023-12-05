from django.db import models

from apps.userauth.models import CustomUser


class Story(models.Model):
    ...


# stories = models.IntegerField(default=0, validators=[
#         MinValueValidator(limit_value=0, message="Stories number cannot be negative!")
#     ])


class Photo(models.Model):
    ...


# photos = models.IntegerField(default=0, validators=[
#         MinValueValidator(limit_value=0, message="Photos number cannot be negative!")
#     ])

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.CharField()
    description = models.CharField(null=True)

    def __str__(self):
        return self.text[:10] + "..."


# posts

class Friend(models.Model):
    ...
# friends = models.IntegerField(default=0, validators=[
#         MinValueValidator(limit_value=0, message="Friends number cannot be negative!")
#     ])
# relate after with userprofile using foreignkey
