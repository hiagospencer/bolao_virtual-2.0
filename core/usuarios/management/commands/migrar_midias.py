import os
from django.core.management.base import BaseCommand
from django.conf import settings
from cloudinary.uploader import upload
from cloudinary.exceptions import Error as CloudinaryError

PASTAS_MEDIA = ['itens_loja', 'logos_loja', 'perfis', 'premios']

class Command(BaseCommand):
    help = 'Migra arquivos da pasta media local para o Cloudinary'

    def handle(self, *args, **kwargs):
        media_root = settings.MEDIA_ROOT

        for pasta in PASTAS_MEDIA:
            caminho_completo = os.path.join(media_root, pasta)
            if not os.path.exists(caminho_completo):
                self.stdout.write(self.style.WARNING(f"Pasta não encontrada: {caminho_completo}"))
                continue

            arquivos = os.listdir(caminho_completo)
            if not arquivos:
                self.stdout.write(self.style.WARNING(f"Nenhum arquivo encontrado em: {caminho_completo}"))
                continue

            for arquivo in arquivos:
                caminho_arquivo = os.path.join(caminho_completo, arquivo)

                if not os.path.isfile(caminho_arquivo):
                    continue  # ignora subpastas

                try:
                    resultado = upload(caminho_arquivo, folder=pasta)
                    url = resultado.get('secure_url')
                    self.stdout.write(self.style.SUCCESS(f"[{pasta}] {arquivo} enviado com sucesso! URL: {url}"))
                except CloudinaryError as e:
                    self.stderr.write(self.style.ERROR(f"Erro ao enviar {arquivo}: {e}"))
