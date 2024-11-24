from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import PlanPagos
from ..serializers import Plan_PagoSerializer


@api_view(['GET'])
def plan_pago_getAll(request):
    plan_pago = PlanPagos.objects.all()
    serializer = Plan_PagoSerializer(plan_pago)
    if(serializer.is_valid()):
        return Response(serializer.data, many = True)
    return Response(serializer.erros, status= status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def plan_pago_getById(request, pk):
    try:
        plan_pago = PlanPagos.objects.get(pk = pk)
    except PlanPagos.DoesNotExist:
        return Response({'error': 'El registro no existe'})
    serializer = Plan_PagoSerializer(plan_pago)
    if(serializer.is_valid()):
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def plan_pago_create(request):
    serializer = Plan_PagoSerializer(data = request.data)
    if(serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, status= status.HTTP_200_OK)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def plan_pago_update(request, pk):
    try:
        plan_pago = PlanPagos.objects.get(pk = pk)
    except PlanPagos.DoesNotExist:
        return Response({'error':'El registro no existe'})
    if(request.method =='PATCH'):
        serializer = Plan_PagoSerializer(plan_pago, data = request.data, partial = True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    elif(request.method == 'PUT'):
        serializer = Plan_PagoSerializer(plan_pago, data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    return Response({'error':'metodo no valido el metodo debe de ser PUT o PATCH'}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def plan_pago_delete(request, pk):
    try:
        plan_pago = PlanPagos.objects.get(pk = pk)
    except PlanPagos.DoesNotExist:
        return Response({'error': 'El registro no existe'})
    plan_pago.delete()
    return Response({'messaje':'El registro a sido eliminado correctamente'}, status= status.HTTP_200_OK)

@api_view(['GET'])
def planPagos_creditos(request , fk):
    try:
        plan_pagos = PlanPagos.objects.filter(credito = fk)
    except PlanPagos.DoesNotExist:
        return Response({'error': 'El cliente no tiene plan de pagos'}, status = status.HTTP_400_BAD_REQUEST)
    serializer = Plan_PagoSerializer(plan_pagos, many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)

    
