from django.db import models
from django.conf import settings

class Feedback(models.Model):

    class TipoFeedback(models.TextChoices):
        GENERAL = "General"
        MEJORA = "Mejora"
        BUG = "Bug"
        SUGERENCIA = "Sugerencia"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Usuario"
    )

    tipo = models.CharField(
        max_length=20,
        choices=TipoFeedback.choices,
        default=TipoFeedback.GENERAL,
        verbose_name="Tipo de feedback"
    )

    mensaje = models.TextField(verbose_name="Mensaje")

    valoracion = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Valoración"
    )

    revisado = models.BooleanField(default=False, verbose_name="Revisado por admin")

    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de envío")

    def __str__(self):
        return f"{self.tipo} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-fecha']
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"