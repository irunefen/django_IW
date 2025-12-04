from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from apptop100.models import Album, Artista, Cancion, Estilo


class Command(BaseCommand):
    help = "Crea/actualiza grupos de administración con permisos predefinidos."

    def handle(self, *args, **options):
        role_matrix = {
            "Moderador solo lectura": {
                Estilo: ["view"],
                Artista: ["view"],
                Album: ["view"],
                Cancion: ["view"],
            },
            "Gestor musical": {
                Estilo: ["view", "add", "change"],
                Artista: ["view", "add", "change"],
                Album: ["view", "add", "change"],
                Cancion: ["view", "add", "change"],
            },
            "Editor senior": {
                Estilo: ["view", "add", "change", "delete"],
                Artista: ["view", "add", "change"],
                Album: ["view", "add", "change"],
                Cancion: ["view", "add", "change", "delete"],
            },
        }

        for role_name, config in role_matrix.items():
            group, created = Group.objects.get_or_create(name=role_name)
            permissions = []

            for model, actions in config.items():
                ct = ContentType.objects.get_for_model(model)
                for action in actions:
                    codename = f"{action}_{model._meta.model_name}"
                    try:
                        perm = Permission.objects.get(content_type=ct, codename=codename)
                        permissions.append(perm)
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Permiso no encontrado: {codename}"))

            group.permissions.set(permissions)
            group.save()

            verb = "creado" if created else "actualizado"
            self.stdout.write(self.style.SUCCESS(f"Grupo {role_name} {verb} con {len(permissions)} permisos."))

        self.stdout.write(self.style.SUCCESS("Roles de administración configurados correctamente."))
