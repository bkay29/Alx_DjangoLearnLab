# LibraryProject/bookshelf/management/commands/create_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

class Command(BaseCommand):
    help = "Create default groups (Editors, Viewers, Admins) and assign bookshelf permissions."

    def handle(self, *args, **options):
        Book = apps.get_model("bookshelf", "Book")
        content_type = ContentType.objects.get_for_model(Book)

        perm_codenames = ["can_view", "can_create", "can_edit", "can_delete"]
        perms = {p.codename: p for p in Permission.objects.filter(content_type=content_type, codename__in=perm_codenames)}

        groups = {
            "Editors": ["can_create", "can_edit", "can_view"],
            "Viewers": ["can_view"],
            "Admins": ["can_view", "can_create", "can_edit", "can_delete"],
        }

        for group_name, p_list in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for codename in p_list:
                perm = perms.get(codename)
                if perm:
                    group.permissions.add(perm)
            group.save()
            self.stdout.write(self.style.SUCCESS(f"Group '{group_name}' ready."))