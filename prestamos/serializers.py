from rest_framework import serializers
from .models import Cliente, DetalleCliente, Prenda, Credito, PlanPagos, Pago, SolicitudCredito

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

class ClienteSerializer(serializers.ModelSerializer):
    detallecliente_set = Detalle_clienteSerializer(many=True, read_only=True)
    prenda_set = PrendaSerializer(many=True, read_only=True)
    credito_set = CreditoSerializer(many=True, read_only=True)

    class Meta:
        model = Cliente
        fields = [
            'id', 'nombre', 'apellidos', 'fecha_nacimiento', 'telefono', 'genero',
            'detallecliente_set', 'prenda_set', 'credito_set'
        ]