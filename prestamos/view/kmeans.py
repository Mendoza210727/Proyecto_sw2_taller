from sklearn.cluster import KMeans
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg, Count, Sum
from ..models import Cliente, Credito, Pago
from ..serializers import ClienteClusterSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count, Q, F
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd

class ClienteClusteringView(APIView):
    def get(self, request):
        try:
            # Obtener datos para el clustering
            clientes_data = []
            
            clientes = Cliente.objects.all()
            
            for cliente in clientes:
                # Obtener todos los pagos asociados al cliente a través de sus créditos
                pagos = Pago.objects.filter(
                    plan_pagos__credito__cliente=cliente
                )
                
                if not pagos.exists():
                    continue
                
                # Calcular métricas
                promedio_dias_atraso = pagos.aggregate(
                    avg_atraso=Avg('dias_atraso')
                )['avg_atraso'] or 0
                
                total_pagos = pagos.count()
                pagos_atrasados = pagos.filter(
                    Q(estado_pago='ATRASADO') | Q(estado_pago='INCUMPLIDO')
                ).count()
                
                porcentaje_pagos_atrasados = (pagos_atrasados / total_pagos * 100) if total_pagos > 0 else 0
                
                total_creditos = Credito.objects.filter(cliente=cliente).count()
                
                clientes_data.append({
                    'cliente': cliente,
                    'features': [
                        promedio_dias_atraso,
                        porcentaje_pagos_atrasados,
                        total_creditos
                    ]
                })
            
            if not clientes_data:
                return Response(
                    {"error": "No hay suficientes datos para realizar el clustering"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Preparar datos para K-means
            X = np.array([cliente['features'] for cliente in clientes_data])
            
            # Normalizar características
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Aplicar K-means
            kmeans = KMeans(n_clusters=3, random_state=42)
            clusters = kmeans.fit_predict(X_scaled)
            
            # Mapear clusters a categorías de clientes
            # Ordenar centroides por promedio_dias_atraso y porcentaje_pagos_atrasados
            centroids = kmeans.cluster_centers_
            cluster_scores = centroids[:, 0] + centroids[:, 1]  # Combinar métricas negativas
            cluster_ranking = np.argsort(cluster_scores)
            
            cluster_mapping = {
                cluster_ranking[0]: 'BUEN_PAGADOR',
                cluster_ranking[1]: 'PAGADOR_REGULAR',
                cluster_ranking[2]: 'MAL_PAGADOR'
            }
            
            # Preparar respuesta
            response_data = []
            for i, cliente_data in enumerate(clientes_data):
                cliente = cliente_data['cliente']
                cluster = clusters[i]
                
                response_data.append({
                    'id': cliente.id,
                    'nombre': cliente.nombre,
                    'apellidos': cliente.apellidos,
                    'cluster_grupo': cluster_mapping[cluster],
                    'promedio_dias_atraso': cliente_data['features'][0],
                    'porcentaje_pagos_atrasados': cliente_data['features'][1],
                    'total_creditos': cliente_data['features'][2]
                })
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"Error al realizar el clustering: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
