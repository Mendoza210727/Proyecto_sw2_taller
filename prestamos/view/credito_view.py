from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from ..models import Credito, Cliente
from ..serializers import CreditoSerializer

@api_view(['GET'])
def credito_getAll(request):
    credito = Credito.objects.all()
    serializer = CreditoSerializer(credito, many = True)
    return Response(serializer.data, status= status.HTTP_200_OK)

@api_view(['GET'])
def credito_getById(request , pk):
    try:
        credito = Credito.objects.get(pk =pk)
    except Credito.DoesNotExist:
        return Response({'error':'el registo no existe'})
    serializer = CreditoSerializer(credito)
    if(serializer.is_valid()):
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def credito_create(request):
    serializer = CreditoSerializer(data = request.data)
    if(serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PUT' , 'PATCH'])
def credito_update(request , pk):
    try:
        credito = Credito.objects.get(pk = pk)
    except Credito.DoesNotExist:
        return Response({'error':'registro no existe'}, status =status.HTTP_400_BAD_REQUEST)
    if(request.method == 'PATCH'):
        serializer = CreditoSerializer(credito, data = request.data, partial = True)
        serializer.save()
        return Response(serializer.data , status = status.HTTP_200_OK)
    elif(request.method == 'PUT'):
        serializer = CreditoSerializer(credito, data = request.data)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response({'error':'metodo no valido'}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def credito_delete(request , pk):
    try:
        credito = Credito.objects.get(pk = pk)
    except Credito.DoesNotExist:
        return Response({'erro':'registro no existe'}, status = status.HTTP_400_BAD_REQUEST)
    credito.delete()
    return Response({'messaje': 'Registro eliminado correctament'}, status = status.HTTP_200_OK)

@api_view(['GET'])
def creditos_clientes(requets, fk):
    try:
        creditos = Credito.objects.filter(cliente = fk)
    except Credito.DoesNotExist:
        return Response({'error': 'El cliente o tiene creditos'}, status= status.HTTP_400_BAD_REQUEST)
    serializer = CreditoSerializer(creditos, many = True)
    return Response (serializer.data, status= status.HTTP_200_OK)


