from django.db import models
from django.utils.translation import gettext_lazy as _


class ListaEspera(models.Model):
    """Modelo para representar la lista de espera"""

    actividad = models.ForeignKey('Actividad', on_delete=models.RESTRICT)

    def __str__(self):
        return f'Lista de espera para {self.actividad}'


class EntradaListaEspera(models.Model):
    """Modelo para representar una entrada a la lista de espera"""

    fechaEntrada = models.DateField(auto_now=True)
    horaEntrada = models.TimeField(auto_now=True)

    listaEspera = models.ForeignKey(ListaEspera, on_delete=models.RESTRICT)
    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.RESTRICT)

    def __str__(self):
        return f'Fecha: {self.fechaEntrada}, Hora: {self.horaEntrada}'
