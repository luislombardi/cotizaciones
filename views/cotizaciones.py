
# views/cotizaciones.py

from flask import Blueprint, render_template

cotizaciones_bp = Blueprint('cotizaciones', __name__)




# Función para obtener datos de cotización
def obtener_cotizacion(ticker):
    try:
        accion = yf.Ticker(ticker)
        print(f"Información de {ticker}: {accion.info}")  # Depuración: Imprimir info
        datos = accion.history(period="5d")  # Obtener los datos del último día
        print(f"Datos históricos de {ticker}: {datos}")  # Depuración: Imprimir datos
        if datos.empty:
            print(f"No se encontraron datos para {ticker}")
            return None
        
        precio_cierre = datos["Close"].iloc[-1]  # Obtener el último precio de cierre
        precio_apertura = datos["Open"].iloc[-1]  # Obtener el precio de apertura
        maximo_dia = datos["High"].iloc[-1]  # Obtener el máximo del día
        minimo_dia = datos["Low"].iloc[-1]  # Obtener el mínimo del día
        volumen = datos["Volume"].iloc[-1]  # Obtener el volumen del día
        
        # Obtener los valores adicionales de la acción
        informacion_accion = accion.info
        rango_52_sem = (informacion_accion.get('fiftyTwoWeekHigh', 'N/A'), informacion_accion.get('fiftyTwoWeekLow', 'N/A'))
        pe_ratio = informacion_accion.get('trailingPE', 'N/A')
        dividendos = informacion_accion.get('dividendYield', 'N/A')
        market_cap = informacion_accion.get('marketCap', 'N/A')
        beta = informacion_accion.get('beta', 'N/A')
        eps = informacion_accion.get('epsTrailingTwelveMonths', 'N/A')
        
        # Crear el diccionario con los datos
        cotizacion_data = {
            'nombre': informacion_accion.get('shortName', ticker),
            'precio': round(precio_cierre, 2),
            'precio_apertura': round(precio_apertura, 2),
            'maximo_dia': round(maximo_dia, 2),
            'minimo_dia': round(minimo_dia, 2),
            'volumen': volumen,
            'rango_52_sem': rango_52_sem,
            'pe_ratio': pe_ratio,
            'dividendos': dividendos,
            'market_cap': market_cap,
            'beta': beta,
            'eps': eps
        }
        
        # Imprimir el diccionario de manera correcta
        print(f"Datos para {ticker}: {cotizacion_data}")  # Ya no es necesario usar str() ni f-string en el diccionario
        
        return cotizacion_data
    except Exception as e:
        print(f"Error al obtener datos para {ticker}: {str(e)}")  # Depuración: Imprimir error
        return None

#@app.route('/')

@cotizaciones_bp.route('/cotizaciones')

def index():
    tickers = ["AAPL", "GOOGL", "TSLA"]  # Lista de tickers
    resultados = []
    
    # Obtener cotización para cada ticker
    for ticker in tickers:
        datos = obtener_cotizacion(ticker)
        if datos:  # Solo agregar los datos si no es None
            resultados.append(datos)
    
    print(f"Datos finales para renderizar: {resultados}")  # Depuración: Imprimir datos que se pasan a la plantilla
    
    # Pasar los datos a la plantilla
    return render_template('index.html', cotizaciones=resultados)

#if __name__ == '__main__':
#    app.run(debug=True)
