from django.contrib import admin
from unesco.models import Iso, Category, Region,States,Site

admin.site.register(Iso)
admin.site.register(Category)
admin.site.register(Region)
admin.site.register(States)
admin.site.register(Site)