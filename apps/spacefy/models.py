from django.db import models


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
    ...


# posts

class Friend(models.Model):
    ...
# friends = models.IntegerField(default=0, validators=[
#         MinValueValidator(limit_value=0, message="Friends number cannot be negative!")
#     ])
# relate after with userprofile using foreignkey
