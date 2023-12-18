from django.contrib import admin

from .models import Gallery, Image, Story, Friend

admin.site.register(Gallery)
admin.site.register(Image)
admin.site.register(Story)
admin.site.register(Friend)
