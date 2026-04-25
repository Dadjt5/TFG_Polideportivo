from django.dispatch import receiver
from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created
from django.conf import settings

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    reset_url = f"{settings.FRONTEND_URL}/reset-password/{reset_password_token.key}"

    message = f"""
Hola,

Has solicitado recuperar tu contraseña.

Pulsa en este enlace:
{reset_url}
"""

    send_mail(
        "Recuperar contraseña",
        message,
        settings.DEFAULT_FROM_EMAIL,
        [reset_password_token.user.email],
        fail_silently=False
    )