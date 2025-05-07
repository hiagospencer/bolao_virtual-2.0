from django.http import JsonResponse

def show_alert(request, type, title, message):
    """Armazena alerta na sessão para mostrar na próxima página"""
    if not request.session.get('global_alerts'):
        request.session['global_alerts'] = []

    alerts = request.session['global_alerts']
    alerts.append({'type': type, 'title': title, 'message': message})
    request.session['global_alerts'] = alerts

def process_alerts(request, context):
    """Adiciona alerts ao contexto template"""
    alerts = request.session.pop('global_alerts', [])
    context['global_alerts'] = alerts
    return context

def json_alert(type, title, message):
    """Retorna JsonResponse com alerta (para AJAX)"""
    return JsonResponse({
        'status': 'alert',
        'alert': {
            'type': type,
            'title': title,
            'message': message
        }
    }, status=200 if type == 'success' else 400)
