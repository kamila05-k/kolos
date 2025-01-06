from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'failed_attempts', 'is_locked', 'is_staff', 'is_superuser', 'last_attempt')
    list_filter = ('is_locked', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    ordering = ('-timestamp',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('-timestamp')

admin.site.register(CustomUser, CustomUserAdmin)
