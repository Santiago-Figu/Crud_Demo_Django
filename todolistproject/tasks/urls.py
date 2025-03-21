from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, UsuarioViewSet

router = DefaultRouter()
#Agregado de rutas 
router.register(r'tasks', TaskViewSet)
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]