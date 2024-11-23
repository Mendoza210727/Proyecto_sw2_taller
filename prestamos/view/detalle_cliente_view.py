from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status

from ..models import DetalleCliente
from ..serializers import Detalle_clienteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


#rutas detalle del cliente
@api_view(['POST'])
def detalle_cliente_create(request):
    serializer = Detalle_clienteSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error':'No se pudo crear el detalle'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def detalle_cliente_all(request):
    detalle = DetalleCliente.objects.all()
    serializer = Detalle_clienteSerializer(detalle, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def detalle_cliente_get(request, fk):
    try:
        detalle = DetalleCliente.objects.filter(fk_cliente = fk)
    except DetalleCliente.DoesNotExist:
        return Response({'error':'Detalles no encontrados'}, status = status.HTTP_400_BAD_REQUEST)
    serializer = Detalle_clienteSerializer(detalle, many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)


@api_view(['PUT , PATCH'])
def detalle_cliente_update(request , fk):
    try:
        detalle = DetalleCliente.objects.filter(fk_cliente = fk)
    except DetalleCliente.DoesNotExist:
        return Response({'error': 'El registro no esxiste'}, status = status.HTTP_400_BAD_REQUEST)
    if(request.method == 'PATCH'):
        serializer = Detalle_clienteSerializer(detalle, data = request.data, patial = True)
        if(serializer.is_valid()):
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status =status.HTTP_404_NOT_FOUND)
    elif(request.method == 'PUT'):
        serializer = Detalle_clienteSerializer(detalle, data = request.data)
        if(serializer.is_valid()):
            return Response(serializer, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Metodo no valido'}, status = status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
def detalle_cliente_delete(request , pk):
    try:
        detalle = DetalleCliente.objects.get(pk = pk )
    except DetalleCliente.DoesNotExist:
        return Response({'error' : 'Registro no encontrado'}, status = status.HTTP_404_NOT_FOUND)
    detalle.delete()
    return Response({'Messaje' : 'Registro eliminado correctamente'}, status =status.HTTP_200_OK)

        
