from django.db import models

# Opciones de género
GENDER_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ('O', 'Otro'),
]

# Opciones de estado de solicitud
SOLICITUD_ESTADO_CHOICES = [
    ('APROBADO', 'Aprobado'),
    ('RECHAZADO', 'Rechazado'),
    ('PENDIENTE', 'Pendiente'),
]

# Opciones de estado del crédito
CREDITO_ESTADO_CHOICES = [
    ('VIGENTE', 'Vigente'),
    ('TERMINADO', 'Terminado'),
    ('INCUMPLIDO', 'Incumplido'),
]

# Opciones de estado del pago
PAGO_ESTADO_CHOICES = [
    ('PENDIENTE', 'Pendiente'),
    ('REALIZADO', 'Realizado'),
    ('ATRASADO', 'Atrasado'),
    ('INCUMPLIDO', 'Incumplido'),
]


class Cliente(models.Model):
    nombre = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=8)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class DetalleCliente(models.Model):
    detalle = models.TextField()
    ocupacion = models.CharField(max_length=150)
    fecha_inicio_ocupacion = models.DateField()
    total_ingresos = models.DecimalField(max_digits=20, decimal_places=2)
    tipo_ocupacion = models.CharField(max_length=150)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Prenda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, related_name="prendas")
    descripcion = models.TextField()
    valor_estimado = models.DecimalField(max_digits=20, decimal_places=2)
    estado = models.CharField(max_length=50)
    fecha_recepcion = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)


class SolicitudCredito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, related_name="solicitudes")
    prenda = models.ForeignKey(Prenda, on_delete=models.SET_NULL, null=True, related_name="solicitudes")
    monto = models.DecimalField(max_digits=20, decimal_places=2)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2)
    estado_solicitud = models.CharField(max_length=50, choices=SOLICITUD_ESTADO_CHOICES)


class Credito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, related_name="creditos")
    solicitud = models.OneToOneField(SolicitudCredito, on_delete=models.CASCADE, related_name="credito")
    prenda = models.ForeignKey(Prenda, on_delete=models.SET_NULL, null=True, related_name="creditos")
    monto = models.DecimalField(max_digits=20, decimal_places=2)
    fecha_aprobacion = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateTimeField()
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2)
    estado_credito = models.CharField(max_length=50, choices=CREDITO_ESTADO_CHOICES)


class PlanPagos(models.Model):
    credito = models.ForeignKey(Credito, on_delete=models.CASCADE, related_name="planes_pagos")
    descripcion = models.CharField(max_length=250)
    cantidad_pagos = models.IntegerField()
    inicio_pago = models.DateField()
    fin_pago = models.DateField()


class Pago(models.Model):
    plan_pagos = models.ForeignKey(PlanPagos, on_delete=models.CASCADE, related_name="pagos")
    fecha_programada = models.DateField()
    fecha_pago = models.DateField(null=True, blank=True)
    monto_pagado = models.DecimalField(max_digits=20, decimal_places=2)
    estado_pago = models.CharField(max_length=50, default='PENDIENTE', choices=PAGO_ESTADO_CHOICES)
    dias_atraso = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Calcular automáticamente los días de atraso
        if self.fecha_pago and self.fecha_programada:
            self.dias_atraso = max((self.fecha_pago - self.fecha_programada).days, 0)
        super().save(*args, **kwargs)
