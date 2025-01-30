# __init__.py en la carpeta views para inicializar el módulo de vistas
# views/__init__.py
from .cotizaciones import cotizaciones_bp
from .volatilidad import volatilidad_bp

__all__ = ['cotizaciones_bp', 'volatilidad_bp']