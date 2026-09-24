"""
Lightweight analytics middleware: records one SiteVisitor row per request
(page path, visitor IP, user, user agent) so the custom admin dashboard
(resume/views.py::admin_dashboard) can show traffic stats. Runs on every
request except admin/static/media/the live-stats polling endpoint itself.
"""


class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path
        # Don't log django-admin, static/media asset requests, or the
        # dashboard's own polling endpoint (that would just spam the table).
        skip = ['/admin/', '/static/', '/media/', '/favicon', '/myadmin/realtime/']
        if not any(path.startswith(s) for s in skip):
            try:
                from .models import SiteVisitor
                # NOTE: X-Forwarded-For is client-supplied and can be
                # spoofed, so treat `ip_address` as "best effort" analytics
                # rather than a trustworthy security signal.
                ip = (
                    request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
                    or request.META.get('REMOTE_ADDR', '')
                )
                SiteVisitor.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    ip_address=ip or None,
                    page=path,
                    session_key=request.session.session_key or '',
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:300],
                )
            except Exception:
                # Analytics logging must never break the actual page request.
                pass
        return response
