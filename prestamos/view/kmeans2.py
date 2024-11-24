from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count, Q
import numpy as np
import random
from typing import List, Tuple
from ..models import Cliente, Pago, Credito

class CustomKMeans:
    def __init__(self, n_clusters: int = 3, max_iters: int = 300, tol: float = 0.0001):
        self.n_clusters = n_clusters
        self.max_iters = max_iters
        self.tol = tol
        self.centroids = None
        self.labels = None
    
    def _euclidean_distance(self, point1: np.ndarray, point2: np.ndarray) -> float:
        """Calcula la distancia euclidiana entre dos puntos"""
        return np.sqrt(np.sum((point1 - point2) ** 2))
    
    def _initialize_centroids(self, X: np.ndarray) -> np.ndarray:
        """Inicializa los centroides usando inicialización aleatoria simple"""
        n_samples = X.shape[0]
        # Elegir índices aleatorios sin repetición
        centroid_indices = np.random.choice(n_samples, size=self.n_clusters, replace=False)
        return X[centroid_indices]
    
    def _assign_clusters(self, X: np.ndarray) -> np.ndarray:
        """Asigna cada punto al cluster más cercano"""
        distances = np.array([
            [self._euclidean_distance(x, centroid) for centroid in self.centroids]
            for x in X
        ])
        return np.argmin(distances, axis=1)
    
    def _update_centroids(self, X: np.ndarray, labels: np.ndarray) -> Tuple[np.ndarray, float]:
        """Actualiza las posiciones de los centroides"""
        new_centroids = np.zeros_like(self.centroids)
        centroid_shift = 0.0
        
        for k in range(self.n_clusters):
            points_in_cluster = X[labels == k]
            if len(points_in_cluster) > 0:
                new_centroids[k] = np.mean(points_in_cluster, axis=0)
            else:
                new_centroids[k] = self.centroids[k]
            
            centroid_shift += self._euclidean_distance(self.centroids[k], new_centroids[k])
        
        return new_centroids, centroid_shift
    
    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """Ajusta el modelo a los datos y devuelve las etiquetas de cluster"""
        # Verificar que hay suficientes datos
        if X.shape[0] < self.n_clusters:
            raise ValueError(f"El número de muestras ({X.shape[0]}) debe ser mayor que el número de clusters ({self.n_clusters})")
        
        # Verificar que no hay valores NaN
        if np.isnan(X).any():
            raise ValueError("Los datos contienen valores NaN")
        
        # Inicializar centroides
        self.centroids = self._initialize_centroids(X)
        
        for _ in range(self.max_iters):
            # Asignar puntos a clusters
            self.labels = self._assign_clusters(X)
            
            # Actualizar centroides
            new_centroids, centroid_shift = self._update_centroids(X, self.labels)
            
            # Verificar convergencia
            if centroid_shift < self.tol:
                break
                
            self.centroids = new_centroids
            
        return self.labels

class CustomClienteClusteringView(APIView):
    def _normalize_data(self, X: np.ndarray) -> np.ndarray:
        """Normaliza los datos usando normalización min-max con manejo de casos especiales"""
        X_min = X.min(axis=0)
        X_max = X.max(axis=0)
        
        # Evitar división por cero
        range_values = X_max - X_min
        range_values[range_values == 0] = 1  # Si el rango es 0, mantener los valores originales
        
        return (X - X_min) / range_values
    
    def get(self, request):
        try:
            # Obtener datos para el clustering
            clientes_data = []
            clientes = Cliente.objects.all()
            
            for cliente in clientes:
                # Obtener pagos del cliente
                pagos = Pago.objects.filter(
                    plan_pagos__credito__cliente=cliente
                )
                
                if not pagos.exists():
                    continue
                
                # Calcular métricas con manejo de valores nulos
                metricas = pagos.aggregate(
                    avg_atraso=Avg('dias_atraso'),
                    total_pagos=Count('id'),
                    pagos_atrasados=Count('id', filter=Q(estado_pago__in=['ATRASADO', 'INCUMPLIDO']))
                )
                
                promedio_dias_atraso = metricas['avg_atraso'] or 0
                total_pagos = metricas['total_pagos']
                pagos_atrasados = metricas['pagos_atrasados']
                
                # Calcular porcentaje con manejo de división por cero
                porcentaje_pagos_atrasados = (pagos_atrasados / total_pagos * 100) if total_pagos > 0 else 0
                total_creditos = Credito.objects.filter(cliente=cliente).count()
                
                clientes_data.append({
                    'cliente': cliente,
                    'features': [
                        float(promedio_dias_atraso),  # Asegurar que son float
                        float(porcentaje_pagos_atrasados),
                        float(total_creditos)
                    ]
                })
            
            if len(clientes_data) < 3:
                return Response(
                    {"error": "Se necesitan al menos 3 clientes con datos de pago para realizar el clustering"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Preparar y normalizar datos
            X = np.array([cliente['features'] for cliente in clientes_data])
            
            # Verificar valores antes de normalizar
            if np.isnan(X).any():
                return Response(
                    {"error": "Los datos contienen valores inválidos"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            X_normalized = self._normalize_data(X)
            
            # Aplicar clustering personalizado
            kmeans = CustomKMeans(n_clusters=3, max_iters=300, tol=0.0001)
            clusters = kmeans.fit_predict(X_normalized)
            
            # Calcular scores para mapeo de clusters
            cluster_scores = []
            for i in range(3):
                mask = clusters == i
                if np.any(mask):
                    score = np.mean(X_normalized[mask][:, :2])  # Solo usar días de atraso y porcentaje
                    cluster_scores.append(score)
                else:
                    cluster_scores.append(0)
            
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
                    'promedio_dias_atraso': round(cliente_data['features'][0], 2),
                    'porcentaje_pagos_atrasados': round(cliente_data['features'][1], 2),
                    'total_creditos': int(cliente_data['features'][2])
                })
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"Error al realizar el clustering: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )