from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from core import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("user.urls")),
    path("", include("book.urls")),
    path("", include("transactions.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
