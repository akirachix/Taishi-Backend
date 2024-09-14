from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from .models import User


@receiver(post_save, sender=User)
def assign_user_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:

            """Add the superuser to the admin group"""

            admin_group, created = Group.objects.get_or_create(name="Admin")
            instance.groups.add(admin_group)

            """ Assign admin permissions"""

            admin_permissions = Permission.objects.filter(
                codename__in=[
                    "view_dashboard",
                    "view_product_metrics",
                    "view_model_metrics",
                    "manage_users",
                    "view_active_users",
                    "view_signups",
                    "view_processing_time",
                    "view_detailed_analytics",
                ]
            )
            instance.user_permissions.set(admin_permissions)
        elif instance.role == "judge":

            """Assign judge group and permissions"""

            judge_group, created = Group.objects.get_or_create(name="Judge")
            instance.groups.add(judge_group)
            judge_permissions = Permission.objects.filter(
                codename__in=[
                    "view_cases",
                    "view_hearings",
                    "schedule_hearings",
                    "view_case_details",
                ]
            )
            instance.user_permissions.set(judge_permissions)
        else:

            """Default user with read-only access"""

            default_group, created = Group.objects.get_or_create(name="Default User")
            instance.groups.add(default_group)
            default_permissions = Permission.objects.filter(codename="view_dashboard")
            instance.user_permissions.set(default_permissions)

        instance.save()
