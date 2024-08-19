from django.contrib import admin
from . models import User, Subject, Post, Bid, Resource

# Register your models here.
admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Post)
admin.site.register(Bid)
admin.site.register(Resource)
