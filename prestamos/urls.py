from django.urls import path
from .view.cliente_view import cliente_create, cliente_all, cliente_get, cliente_update, cliente_delete
from .view.prenda_view import prenda_all, prenda_get, prenda_create, prenda_update, prenda_delete, prendas_clientes
from .view.detalle_cliente_view import detalle_cliente_create, detalle_cliente_get, detalle_cliente_all, detalle_cliente_update, detalle_cliente_delete
from .view.credito_view import credito_getAll,credito_getById,credito_create,credito_update,credito_delete, creditos_clientes
from .view.plan_pago_view import plan_pago_create, plan_pago_getAll, plan_pago_getById, plan_pago_update, plan_pago_delete, planPagos_creditos
from .view.pago_view import pago_create, pago_getAll, pago_getById, pago_update, pago_delete, pagos_planPagos
from .view.evaluacion_view import agrupar_clientes
from .view.solicitud_credito_view import solicitud_creaate
from .view.kmeans import ClienteClusteringView
from .view.kmeans2 import CustomClienteClusteringView


urlpatterns = [
    # rutas de Clientes
    path('clientes', cliente_all, name = 'clientes'),
    path('clientes/<int:pk>', cliente_get, name = 'cliente'),
    path('clientes/create', cliente_create, name = 'cliente-creaate'),
    path('clientes/update/<int:pk>', cliente_update, name = 'clientes-update'),
    path('clientes/delete/<int:pk>', cliente_delete, name = 'clientes-delete'),
    # rutas de Prenda
    path('prendas/', prenda_all, name = 'prendas'),
    path('prendas/<int:pk>', prenda_get, name='prenda'),
    path('prendas/clientes/<int:fk>',prendas_clientes , name='prenda-clientes'),
    path('prendas/create', prenda_create, name = 'prendas-create'),
    path('prendas/update/<int:pk>', prenda_update, name='prendas-update'),
    path('prendas/delete/<int:pk>', prenda_delete, name = 'prendas-delete'),
    #rutas de detalle_cliente
    path('detalle-cliente/', detalle_cliente_all, name = 'detalle-cliente'),
    path('detalle-cliente/<int:fk>', detalle_cliente_get, name='detalle-cliente'),
    path('detalle-cliente/create', detalle_cliente_create, name = 'detalle-cliente-create'),
    path('deatalle-cliente/update/<int:pk>', detalle_cliente_update, name = 'deatelle-cliente-update'),    
    path('deatalle-cliente/delete/<int:pk>', detalle_cliente_delete, name = 'deatelle-cliente-delete'),    
    #rutas de creditos 
    path('credito/', credito_getAll, name = 'credito'),
    path('credito/<int:pk>/', credito_getById, name = ''),
    path('credito/create', credito_create, name = ''),
    path('credito/update/<int:pk>', credito_update, name = ''),
    path('credito/delete/<int:pk>', credito_delete, name = ''),
    path('creditos/cliente/<int:fk>', creditos_clientes, name ='creditos-clientes'),


    #rutas de plan de pagos
    path('plan-pago/', plan_pago_getAll, name = ''),
    path('plan-pago/<int:pk>', plan_pago_getById, name = ''),
    path('plan-pago/create/', plan_pago_create, name = ''),
    path('plan-pago/update/<int:pk>', plan_pago_update, name = ''),
    path('plan-pago/delete/<int:pk>', plan_pago_delete, name = ''),
    path('plan-pago/credito/<int:fk>',planPagos_creditos, name=""),

    #rutas de pagos 
    path('pago/', pago_getAll, name = ''),
    path('pago/<int:pk>/', pago_getById, name = ''),
    path('pago/create/', pago_create, name = ''),
    path('pago/update/<int:pk>', pago_update, name = ''),
    path('pago/delete/<int:pk>', pago_delete, name = ''),
    path('pago/planPago/<int:fk>', pagos_planPagos, name= '') ,


    path ('solicitud/', solicitud_creaate, name= 'solicitud-create') ,
    #ruta de k-means


    path('clientes/clustering/', ClienteClusteringView.as_view(), name = 'cliente-clustering' ),
    path('clientes/custom-clustering/', CustomClienteClusteringView.as_view(), name='cliente-custom-clustering'),


]

