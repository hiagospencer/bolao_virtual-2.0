from django.core.exceptions import RequestDataTooBig

class MessageSystem:
    @staticmethod
    def add_message(request, type, content):
        """Adiciona mensagem à sessão"""
        if not request.session.get('custom_messages'):
            request.session['custom_messages'] = []

        messages = request.session['custom_messages']
        messages.append({'type': type, 'content': content})
        request.session['custom_messages'] = messages
        request.session.modified = True

    @staticmethod
    def get_messages(request):
        """Obtém e limpa mensagens da sessão"""
        messages = request.session.pop('custom_messages', [])
        return messages

    @staticmethod
    def has_messages(request):
        """Verifica se existem mensagens"""
        return bool(request.session.get('custom_messages'))
