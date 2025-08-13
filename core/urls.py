from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI


from ap_solicitar.api_solicitar_website import solicitar_router, contacto_router   
from usuario.api_usuarios import auth_router, cliente_router

api = NinjaAPI()

api.add_router("/solicitar/", solicitar_router)
api.add_router("/cont/", contacto_router)
api.add_router("/clientes/", cliente_router)
api.add_router("/auth/", auth_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)