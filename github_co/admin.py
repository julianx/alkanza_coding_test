from django.contrib import admin
from github_co.models import User, Repos, Location


class UserAdmin(admin.ModelAdmin):
    raw_id_fields = ("repos", 'location')
    search_fields = ('username', 'location__name')
    list_display = ('username', 'colombian')


admin.site.register(User, UserAdmin)
