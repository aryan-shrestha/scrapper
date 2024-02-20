from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from account.views import dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('company/', include('company.urls', namespace='company')),
    path('scrapper/', include('scrapper.urls', namespace='scrapper')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)