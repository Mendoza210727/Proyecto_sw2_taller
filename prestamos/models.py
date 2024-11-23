from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=80, blank = False)
    apellidos = models.CharField(max_length=200, blank = False)
    fecha_nacimiento = models.DateField(blank=False)
    telefono = models.CharField( max_length=8, blank=False)
    genero = models.CharField(max_length=1, blank=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class DetalleCliente(models.Model):
    detalle = models.TextField(blank = False)
    ocupacion = models.CharField(max_length=150, blank= False)
    fecha_inicio_ocupacion =  models.DateField(blank=False)
    total_ingresos = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    tipo_ocupacion = models.CharField(max_length=150, blank=False)
    fk_cliente = models.ForeignKey(Cliente, on_delete = models.SET_NULL, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class Prenda(models.Model):
    descripcion = models.TextField(blank=False)
    valor_estimado = models.DecimalField(max_digits=10, decimal_places=2, blank=False),
    estado = models.CharField(max_length=50, blank=False)
    fecha_resepcion = models.DateTimeField( auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null= True)
    fk_cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null= True)

class SolicitudCredito(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank= False)
    fecha_solicitud = models.DateTimeField()
    fecha_aprobacion = models.DateTimeField()
    tasa_interes = models.DecimalField(max_digits=10, decimal_places = 0, blank= False)
    estado_solicitud = models.CharField(
        max_length= 50, blank= False,
        choices = [
            ('APROBADO' , 'Aprobado'),
            ('RECHAZADO', 'Rechazado'),
            ('PENDIENTE', 'Pendiente')
        ]
    )
    fk_cliente = models.ForeignKey(Cliente, on_delete = models.SET_NULL, null = True)
    fk_prenda = models.ForeignKey(Prenda, on_delete = models.SET_NULL, null = True)


class Credito(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    fecha_aprobacion = models.DateTimeField()
    fecha_vencimiento = models.DateTimeField()
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2, help_text="Porcentaje de la tasa de interés")
    estado_credito = models.CharField(
        max_length=150, blank=False,
        choices=[
            ('VIGENTE', 'Vigente'),
            ('TERMINADO', 'Terminado'),
            ('INCUMPLIDO' ,'Incumplido')
        ]
    )
    fk_cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    fk_prenda = models.ForeignKey(Prenda, on_delete=models.SET_NULL, null=True)
    fk_solicitud_credito = models.ForeignKey(SolicitudCredito, on_delete = models.SET_NULL, null = True)

class PlanPagos(models.Model):
    descripcion = models.CharField(max_length=250)
    cantidad_pagos = models.DecimalField(max_digits=5, decimal_places=0)  # Añadir max_digits y decimal_places
    inicio_pago = models.DateField()
    fin_pago = models.DateField()
    fk_credito = models.ForeignKey(Credito, on_delete=models.SET_NULL, null=True)

class Pago(models.Model):
    fecha_programada = models.DateField()
    fecha_pago = models.DateField()
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    estado_pago = models.CharField(max_length=50, blank=False, default='Pendiente')
    fk_plan_pagos = models.ForeignKey(PlanPagos, on_delete=models.SET_NULL, null=True)






