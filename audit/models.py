from django.db import models


from django.db import models

class ApiAuditLog(models.Model):
    endpoint_name = models.CharField(max_length=255, db_index=True)
    path = models.TextField()
    method = models.CharField(max_length=10, db_index=True)

    requesting_ip = models.GenericIPAddressField(null=True, blank=True)
    status_code = models.PositiveSmallIntegerField(db_index=True)

    is_error = models.BooleanField(default=False, db_index=True)

    # response payload (success/error), keep as JSON where possible
    data = models.JSONField(null=True, blank=True)

    duration_ms = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "api_audit_log"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.method} {self.endpoint_name} [{self.status_code}]"