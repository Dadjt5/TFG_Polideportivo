from django.contrib import admin

from polideportivo.models import (
    Actividad, Agenda, Bono, Configuracion, Deporte, Descuento, Favorito,
    Foro, Instalacion, ListaEspera, Asistencia, Canal, UsuarioCanal, 
    EntradaListaEspera, TarifaTDA, Monitor, Notificacion, Pago, TarifaActividad, 
    TarifaInstalacion, TDA, UsuarioFinal, AbonoDeportivo, AbonoVerano, Pabellon, 
    ReservaActividad, Alquiler, Administrador, CompraAbono, CompraBono, Sesion,
    Mensaje, ActividadComun, GrupoReducido, Fisioterapia, MapaReservas, Feedback
)

admin.site.register(Feedback)

admin.site.register(AbonoDeportivo)
admin.site.register(AbonoVerano)
admin.site.register(CompraAbono)

admin.site.register(Actividad)
admin.site.register(Sesion)
admin.site.register(Asistencia)

admin.site.register(Agenda)
admin.site.register(MapaReservas)

admin.site.register(Bono)
admin.site.register(CompraBono)

admin.site.register(Configuracion)

admin.site.register(Deporte)

admin.site.register(Descuento)

admin.site.register(Favorito)

admin.site.register(Foro)
admin.site.register(Canal)
admin.site.register(UsuarioCanal)
admin.site.register(Mensaje)

admin.site.register(Instalacion)
admin.site.register(Pabellon)

admin.site.register(ListaEspera)
admin.site.register(EntradaListaEspera)

admin.site.register(Notificacion)

admin.site.register(Pago)

admin.site.register(ReservaActividad)
admin.site.register(Alquiler)

admin.site.register(TarifaTDA)

admin.site.register(TarifaActividad)
admin.site.register(ActividadComun)
admin.site.register(GrupoReducido)
admin.site.register(Fisioterapia)

admin.site.register(TarifaInstalacion)

admin.site.register(TDA)

admin.site.register(Monitor)
admin.site.register(UsuarioFinal)
admin.site.register(Administrador)
