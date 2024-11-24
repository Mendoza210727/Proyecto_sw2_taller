from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Pago
from ..serializers import PagosSerializer

@api_view(['GET'])
def pago_getAll(request):
    pago = Pago.objects.all()
    serializer = PagosSerializer(pago, many = True)
    if(serializer.is_valid()):
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def pago_getById(request, pk):
    try:
        pago = Pago.objects.get(pk =pk)
    except Pago.DoesNotExist:
        return Response({'error':'El registro no existe'}, status = status.HTTP_400_BAD_REQUEST)
    serializer = PagosSerializer(pago)
    if(serializer.is_valid()):
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def pago_create(request):
    serializer = PagosSerializer(data = request.data)
    if(serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def pago_update(request, pk):
    try:
        pago = Pago.objects.get(pk = pk)
    except Pago.DoesNotExist:
        return Response({'error':'El registro no existe'})
    if(request.method == 'PATCH'):
        serializer = PagosSerializer(pago , data = request.data, partial = True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    elif(request.method == 'PUT'):
        serializer = PagosSerializer(pago, data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    return Response({'error':'Metodo no valido , los metodos deben de ser PUT , PATCH'})

@api_view(['DELETE'])
def pago_delete(request, pk):
    try:
        pago = Pago.objects.get(pk = pk)
    except Pago.DoesNotExist:
        return Response({'error':'El registro no es existe'})
    pago.delete()
    return Response({'messaje':'Registro eliminado con existo'})

@api_view(['GET'])
def pagos_planPagos(request, fk):
    try:
        pagos = Pago.objects.filter(plan_pagos = fk)
    except Pago.DoesNotExist:
        return Response({'error': ' El Plan de pagos no tiene pagos registrados'}, status = status.HTTP_400_BAD_REQUEST)
    serializer = PagosSerializer(pagos, many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)
