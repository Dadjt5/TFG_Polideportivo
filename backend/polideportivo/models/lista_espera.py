from django.db import models
from django.utils.translation import gettext_lazy as _


class ListaEspera(models.Model):
    """Modelo para representar la lista de espera"""

    actividad = models.ForeignKey('Actividad', on_delete=models.CASCADE, related_name='lista_espera')

    def __str__(self):
        return f'Lista de espera para {self.actividad}'

    def salirLista(self, usuario):
        self.registro.filter(usuarioFinal=usuario).delete()
        
    def siguienteUsuario(self):
        return self.registro.order_by('fechaEntrada', 'horaEntrada').first()


class EntradaListaEspera(models.Model):
    """Modelo para representar una entrada a la lista de espera"""

    fechaEntrada = models.DateField(auto_now=True)
    horaEntrada = models.TimeField(auto_now=True)

    listaEspera = models.ForeignKey(ListaEspera, on_delete=models.RESTRICT, related_name="registro")
    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.RESTRICT, related_name="lista_espera")

    def __str__(self):
        return f'Fecha: {self.fechaEntrada}, Hora: {self.horaEntrada}'
    
    @classmethod
    def contar(cls):
        return cls.objects.count()

    class Meta:
        unique_together = ('listaEspera', 'usuarioFinal')