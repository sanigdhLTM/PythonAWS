from django.contrib import admin

# Register your models here.
# audit/admin.py
from django.contrib import admin
from audit.models import ApiAuditLog

@admin.register(ApiAuditLog)
class ApiAuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "method", "endpoint_name", "status_code", "is_error", "requesting_ip", "duration_ms")
    list_filter = ("method", "status_code", "is_error", "created_at")
    search_fields = ("endpoint_name", "path", "requesting_ip")
