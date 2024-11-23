from django.shortcuts import render
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from ..models import Cliente
from ..serializers import ClienteSerializer

#rutas  de cliente
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cliente_create(request):
    serializer = ClienteSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cliente_all(request):
    clientes = Cliente.objects.all()
    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def cliente_get(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response({'error': 'No se encontro el cliente'}, status = status.HTTP_404_NOT_FOUND)
    serializer = ClienteSerializer(cliente)
    return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['PATCH', 'PUT'])
def cliente_update(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response({'error':'No se encontro el cliente'}, ststus = status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH':
        serializer = ClienteSerializer(cliente, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.error, status = status.HTTP_404_NOT_FOUND)
    elif request.method == 'PUT':
        serializer = ClienteSerializer(cliente, data = request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
def cliente_delete(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response({'errors':'No se encontro el cliente'}, status = status.HTTP_404_NOT_FOUND)
    cliente.delete()
    return Response({'mensaje':'Cliente eliminado correctamente'}, status = status.HTTP_204_NO_CONTENT)