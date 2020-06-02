from django.contrib import admin
from django.contrib.sites.models import Site

from  .models import Contact, Blogpost
# Register your models here.

admin.site.register(Contact)
admin.site.register(Blogpost)