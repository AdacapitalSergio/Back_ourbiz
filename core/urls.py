from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI


from ap_solicitar.api_solicitar_website import solicitar_router, contacto_router   
from usuario.api_usuarios import auth_router, usuario_router, empresa_router
from funcionario.api_funcionario import funcionario_router
from servico.api_servico import router_servicos

api = NinjaAPI()

api.add_router("/auth/", auth_router)
api.add_router("/usuario/", usuario_router)
api.add_router("/solicitar/", solicitar_router)
api.add_router("/contacto/", contacto_router)
api.add_router("/empresa/", empresa_router)
api.add_router("/funcionario/", funcionario_router)
api.add_router("/servicos/", router_servicos)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)