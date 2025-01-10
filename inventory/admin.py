from django.contrib import admin
from .models import Company, User, Inventory

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'company', 'special_code', 'app_usage_period', 'imei_code', 'is_active')
    search_fields = ('username', 'email', 'special_code', 'company__name')
    list_filter = ('company', 'is_active', 'app_usage_period')
    ordering = ('-date_joined',)
    readonly_fields = ('special_code', 'date_joined', 'last_login')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(company=request.user.company)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'barcode', 'quantity', 'user', 'timestamp')
    search_fields = ('barcode', 'user__username')
    list_filter = ('timestamp', 'user')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(user=request.user)
