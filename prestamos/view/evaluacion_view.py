
from django.shortcuts import render
from django.http import JsonResponse
from ..models import Cliente, DetalleCliente, Prenda, Credito
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
import numpy as np
import pandas as pd
from ..serializers import ClienteSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def agrupar_clientes(request):
    # Obtenemos los datos de clientes con las relaciones necesarias
    clientes = Cliente.objects.prefetch_related('detallecliente_set').all()

    # Preparamos los datos para K-means usando detalles relevantes del cliente
    data = []
    for cliente in clientes:
        # Extraemos ingresos y tiempo en ocupación como características de ejemplo
        detalle = cliente.detallecliente_set.first()
        if detalle:
            ingresos = detalle.total_ingresos
            tiempo_ocupacion = (np.datetime64('today') - np.datetime64(detalle.fecha_inicio_ocupacion)).astype('timedelta64[Y]').astype(int)
            data.append([ingresos, tiempo_ocupacion])

    # Convertimos a array de NumPy y escalamos los datos
    data = np.array(data)
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)

    # Definimos el número de clusters para K-means
    kmeans = KMeans(n_clusters=3, random_state=0)
    kmeans.fit(data_scaled)
    labels = kmeans.labels_

    # Añadimos los grupos de K-means a la respuesta para cada cliente
    clientes_con_grupo = []
    for idx, cliente in enumerate(clientes):
        cliente_data = ClienteSerializer(cliente).data
        cliente_data['grupo_kmeans'] = int(labels[idx])
        clientes_con_grupo.append(cliente_data)

    # Retornamos la lista de clientes con sus grupos K-means
    return Response(clientes_con_grupo)