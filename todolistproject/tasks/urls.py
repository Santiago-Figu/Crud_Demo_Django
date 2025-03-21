from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.vistas.task import TaskViewSet
from tasks.vistas.usuario import UsuarioViewSet 

router = DefaultRouter()
#Agregado de rutas 
router.register(r'tasks', TaskViewSet)
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]