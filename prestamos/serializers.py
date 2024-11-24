from rest_framework import serializers
from .models import Cliente, DetalleCliente, Prenda, Credito, PlanPagos, Pago, SolicitudCredito
from decimal import Decimal, ROUND_HALF_UP


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class Detalle_clienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCliente
        fields = '__all__'

class PrendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prenda
        fields = '__all__'

class CreditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credito
        fields = '__all__'

class Plan_PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanPagos
        fields = '__all__'

class PagosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'


class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudCredito
        fields = '__all__'


#algoritmo de Clasificacion K-means

""" class KMeansClusterSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="ID del cliente")
    nombre = serializers.CharField(max_length=80, help_text="Nombre del cliente")
    apellidos = serializers.CharField(max_length=200, help_text="Apellidos del cliente")
    total_creditos = serializers.IntegerField(help_text="Número total de créditos del cliente")
    monto_promedio_credito = serializers.DecimalField(max_digits=20, decimal_places=2, help_text="Monto promedio de créditos")
    total_pagos = serializers.IntegerField(help_text="Número total de pagos realizados")
    cluster = serializers.IntegerField(help_text="Cluster asignado por el algoritmo K-Means") """



class ClienteClusterSerializer(serializers.ModelSerializer):
    cluster_grupo = serializers.CharField(read_only=True)
    promedio_dias_atraso = serializers.FloatField(read_only=True)
    porcentaje_pagos_atrasados = serializers.FloatField(read_only=True)
    total_creditos = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'apellidos', 'cluster_grupo', 'promedio_dias_atraso', 
                 'porcentaje_pagos_atrasados', 'total_creditos']