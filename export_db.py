import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bolao_virtual.settings')
django.setup()

with open("db.json", "w", encoding="utf-8") as f:
    call_command("dumpdata", "--exclude", "contenttypes", "--exclude", "auth.permission", "--exclude", "admin.logentry", "--exclude", "sessions.session", indent=2, stdout=f)

print("✅ Exportado com sucesso como db.json (UTF-8, sem dados internos do Django)")
