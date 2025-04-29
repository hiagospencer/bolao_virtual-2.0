# apps/estatisticas/middleware.py
from django.utils import timezone
from .models import VisitaSite
from usuarios.models import Usuario

class RastreamentoVisitasMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Registrar visita antes de processar a requisição
        if not request.path.startswith('/admin/') and not request.path.startswith('/static/'):
            user = request.user if request.user.is_authenticated else None

            VisitaSite.objects.create(
                usuario=user,
                ip=self.get_client_ip(request),
                pagina=request.path,
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
