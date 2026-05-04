# audit/middleware.py
import json
import time
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

from audit.models import ApiAuditLog


class ApiAuditMiddleware(MiddlewareMixin):
    """
    Logs API calls into DB with endpoint_name, ip, status_code, response data.

    Order: request passes top->bottom; response passes bottom->top. [1](https://stackoverflow.com/questions/33328656/django-type-object-http404-has-no-attribute-get)[2](https://www.geeksforgeeks.org/python/how-to-fix-attributeerror-object-has-no-attribute/)
    """

    # You can tune these:
    API_PREFIXES = ("/blog/",)            # log only these paths (adjust to your routing)
    EXCLUDE_PREFIXES = ("/admin/", "/static/", "/media/")
    MAX_TEXT_LEN = 5000                 # truncate non-JSON response content

    def process_request(self, request):
        request._audit_start = time.monotonic()

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Runs after URL resolution but before the view. Useful to capture endpoint name. [2](https://www.geeksforgeeks.org/python/how-to-fix-attributeerror-object-has-no-attribute/)
        """
        request._audit_view_func = view_func

    def process_exception(self, request, exception):
        """
        Called if the view raises an exception. We'll mark it so response logging can include error. [2](https://www.geeksforgeeks.org/python/how-to-fix-attributeerror-object-has-no-attribute/)
        """
        request._audit_exception = exception
        return None  # let Django/DRF handle the exception

    def process_response(self, request, response):
        try:
            path = getattr(request, "path", "") or ""

            # Decide whether to log this request
            if self._should_skip(path):
                return response

            endpoint_name = self._get_endpoint_name(request)
            requesting_ip = self._get_client_ip(request)

            status_code = getattr(response, "status_code", 0) or 0
            is_error = status_code >= 400 or hasattr(request, "_audit_exception")

            duration_ms = None
            start = getattr(request, "_audit_start", None)
            if start is not None:
                duration_ms = int((time.monotonic() - start) * 1000)

            data = self._extract_response_data(response)

            ApiAuditLog.objects.create(
                endpoint_name=endpoint_name,
                path=path,
                method=getattr(request, "method", "") or "",
                requesting_ip=requesting_ip,
                status_code=status_code,
                is_error=is_error,
                data=data,
                duration_ms=duration_ms,
            )
        except Exception:
            # NEVER break the API if audit logging fails
            pass

        return response

    # ---------------- helpers ----------------

    def _should_skip(self, path: str) -> bool:
        # exclude admin/static/media always
        if path.startswith(self.EXCLUDE_PREFIXES):
            return True

        # log only API endpoints
        if self.API_PREFIXES and not path.startswith(self.API_PREFIXES):
            return True

        return False

    def _get_endpoint_name(self, request) -> str:
        # Preferred: route name from resolver_match (e.g. "blog-detail", "category-list")
        rm = getattr(request, "resolver_match", None)
        if rm:
            if rm.view_name:
                return rm.view_name
            if rm.url_name:
                return rm.url_name

        # Fallback: view function/class name if captured in process_view
        view_func = getattr(request, "_audit_view_func", None)
        if view_func is not None:
            # DRF's as_view attaches .cls on the function in many cases
            view_cls = getattr(view_func, "cls", None)
            if view_cls:
                return view_cls.__name__
            return getattr(view_func, "__name__", "unknown")

        # Last resort
        return getattr(request, "path", "unknown")

    def _get_client_ip(self, request) -> str | None:
        # If behind proxy/load balancer, X-Forwarded-For may contain real client IP
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            # first ip is original client
            return xff.split(",")[0].strip()

        return request.META.get("REMOTE_ADDR")

    def _extract_response_data(self, response: HttpResponse):
        """
        Try to store JSON data if possible; else store text (truncated).
        """
        # DRF Response often has `.data`
        if hasattr(response, "data"):
            try:
                # response.data may be dict/list/ErrorDetail etc.
                return response.data
            except Exception:
                pass

        # Otherwise decode JSON from content if content-type is JSON
        try:
            content_type = (response.get("Content-Type") or "").lower()
            if "application/json" in content_type:
                raw = response.content.decode("utf-8", errors="ignore")
                return json.loads(raw) if raw else None
        except Exception:
            pass

        # Fallback: store text content (truncated)
        try:
            raw = response.content.decode("utf-8", errors="ignore")
            if raw and len(raw) > self.MAX_TEXT_LEN:
                raw = raw[: self.MAX_TEXT_LEN] + "...(truncated)"
            return {"text": raw} if raw else None
        except Exception:
            return None