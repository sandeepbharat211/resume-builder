from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Django's built-in admin is moved to /django-admin/ (still available
    # for raw DB management), and /admin/ now redirects to our own custom
    # admin dashboard (resume.views.admin_dashboard) instead of Django's
    # default admin login page.
    path('django-admin/', admin.site.urls),
    path('admin/', RedirectView.as_view(pattern_name='admin_dashboard', permanent=False)),
    path('', include('resume.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

