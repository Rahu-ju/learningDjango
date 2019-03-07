from django.contrib import admin
from .models import Join
# Register your models here.
class JoinAdmin(admin.ModelAdmin):
    list_display = ['email', 'friend', 'timestamp', 'updated']
    class Meta:
        model = Join
admin.site.register(Join, JoinAdmin)
