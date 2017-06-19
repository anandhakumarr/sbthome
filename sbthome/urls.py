from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from admindashboard import urls as admin_urls
from homepage import urls as home_urls

urlpatterns = [
    url(r'^sbtadmin/', admin.site.urls),
    url(r'^', include(home_urls, namespace='homepage')),
    url(r'^admin/', include(admin_urls, namespace='admindashboard')),
]
 # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
