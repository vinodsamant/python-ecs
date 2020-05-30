from django.contrib import admin

from contest_categories.models import ContestCategory, ContestSubCategory

# register ContestCategory Model
admin.site.register(ContestCategory)

# register ContestSubCategory Model
admin.site.register(ContestSubCategory)
