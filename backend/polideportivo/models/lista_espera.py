from django.db import models
from django.utils.translation import gettext_lazy as _


class ListaEspera(models.Model):
    """Modelo para representar la lista de espera"""

    actividad = models.OneToOneField('Actividad', on_delete=models.CASCADE, related_name='lista_espera')

    def __str__(self):
        return f'Lista de espera para {self.actividad}'

    # Función para añadir un usuario a la lista de espere
    def nuevaEntrada(self, usuario):
        if self.registro.filter(usuarioFinal=usuario).exists():
            return None

        EntradaListaEspera.objects.create(usuarioFinal=usuario, listaEspera=self)
        return self.registro.count()

    # Función para sacar a un usuario de la lista de espera
    def salirLista(self, usuario):
        if self.registro.filter(usuarioFinal=usuario).exists():
            self.registro.filter(usuarioFinal=usuario).delete()

    # Función para obtener el usuario siguiente de la lista de espera
    def siguienteUsuario(self):
        entrada = self.registro.order_by('fechaEntrada', 'horaEntrada').first()

        if not entrada:
            return None

        entrada.delete()
        return entrada


class EntradaListaEspera(models.Model):
    """Modelo para representar una entrada a la lista de espera"""

    fechaEntrada = models.DateField(auto_now_add=True)
    horaEntrada = models.TimeField(auto_now_add=True)

    listaEspera = models.ForeignKey(ListaEspera, on_delete=models.CASCADE, related_name="registro")
    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.CASCADE, related_name="lista_espera")

    def __str__(self):
        return f'Fecha: {self.fechaEntrada}, Hora: {self.horaEntrada}'
    
    # Función para contar el número de entradas en todas las listas
    @classmethod
    def contar(cls):
        return cls.objects.count()

    class Meta:
        unique_together = ('listaEspera', 'usuarioFinal')
        ordering = ['fechaEntrada', 'horaEntrada']