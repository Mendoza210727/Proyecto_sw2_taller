from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Prenda
from ..serializers import PrendaSerializer


@api_view(['POST'])
def prenda_create(request):
    serializer = PrendaSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def prenda_all(request):
    prendas = Prenda.objects.all()
    serializer = PrendaSerializer(prendas, any=True)
    return Response(serializer.data, status = status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def prenda_get(request, pk):
    try:
        prenda = Prenda.objects.get(pk=pk)
    except Prenda.DoesNotExist:
        return Response({'error':'Prenda no encontrada'}, status = status.HTTP_404_NOT_FOUND)
    serializer = PrendaSerializer(prenda)
    return Response(serializer.data, status =status.HTTP_200_OK)

@api_view(['GET'])
def prenda_get_fk(request, fk):
    try:
        prenda = Prenda.objects.filter(fk_cliente = fk)
    except Prenda.DoesNotExist:
        return Response({'error':'Prenda no encontrada'}, status = status.HTTP_404_NOT_FOUND)
    serializer = PrendaSerializer(prenda, many= True)
    return Response(serializer.data, status =status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
def prenda_update(request, pk):
    try:
        prenda = Prenda.objects.get(pk=pk)
    except Prenda.DoesNotExist:
        return Response({'error':'Prenda no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    if request.methdo == 'PATCH':
        serializer = PrendaSerializer(data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response({'error':'Metodo no valido'}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        serializer = PrendaSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_202_ACCEPTED)
        return Response({'error':'Metodo no valido'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
def prenda_delete(request, pk):
    try:
        prenda = Prenda.objects.get(pk=pk)
    except Prenda.DoesNotExist:
        return Response({'error':'Prenda no encontrada'}, status = status.HTTP_404_NOT_FOUND)
    prenda.delete()
    return Response({'message':'Prenda eliminada con exito'}, status = status.HTTP_200_OK)

