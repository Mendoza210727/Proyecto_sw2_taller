from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import SolicitudCredito
from ..serializers import SolicitudSerializer


@api_view(['GET'])
def solicitud_getAll(request):
    solicitud = SolicitudCredito.objects.all()
    serializer = SolicitudSerializer(solicitud, many = True)
    if(serializer.is_valid()):
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def solicitud_getById(request , pk):
    try:
        solicitud = SolicitudCredito.objects.get(pk = pk)
    except SolicitudCredito.DoesNotExist:
        return Response({'error':'El registro no existe'}, status = status.HTTP_400_BAD_REQUEST)
    serializer = SolicitudSerializer(solicitud)
    if(serializer.is_valid()):
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def solicitud_creaate(request):
    serializer = SolicitudSerializer(data = request.data)
    if(serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, staus = status.HTTP_200_OK)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH', 'PUT'])
def solicitud_update(request, pk):
    try:
        solicitud = SolicitudCredito.objects.get(pk = pk)
    except SolicitudCredito.DoesNotExist:
        return Response({'error':'El registro no existe'})
    if(request.method == 'PATCH'):
        serializer = SolicitudSerializer(solicitud, data = request.data, partial =True)
        if(serializer.is_valid()):
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, staus = status.HTTP_400_BAD_REQUEST)
    elif(request.method == 'PUT'):
        serializer = SolicitudSerializer(solicitud, data = request.data)
        if(serializer.is_valid()):
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Metodo no valido el metodo deve de se PUT o PATCH'}, staus = status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def solicitud_delete(request, pk):
    try:
        solicitud = SolicitudCredito.objects.get(pk = pk)
    except SolicitudCredito.DoesNotExist:
        return Response({'error':'El registro no existe'}, status = status.HTTP_400_BAD_REQUEST)
    solicitud.delete
    return Response({'messaje':'El registro se a eliinado exitosamente'})