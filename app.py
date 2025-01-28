
from flask import Flask, render_template
import yfinance as yf

app = Flask(__name__)

# Función para obtener datos de cotización
def obtener_cotizacion(ticker):
    try:
        accion = yf.Ticker(ticker)
        print(f"Información de {ticker}: {accion.info}")  # Depuración: Imprimir info
        datos = accion.history(period="5d")  # Obtener los datos de los últimos 5 días
        print(f"Datos históricos de {ticker}: {datos}")  # Depuración: Imprimir datos
        if datos.empty:
            print(f"No se encontraron datos para {ticker}")
            return None
        precio_cierre = datos["Close"].iloc[-1]  # Obtener el último precio de cierre
        return {
            "nombre": accion.info.get("shortName", ticker),  # Usar el ticker si no hay nombre
            "precio": round(precio_cierre, 2)  # Redondear el precio a 2 decimales
        }
    except Exception as e:
        print(f"Error al obtener datos para {ticker}: {str(e)}")  # Depuración: Imprimir error
        return None

@app.route('/')
def index():
    tickers = ["AAPL", "GOOGL", "TSLA"]  # Lista de tickers
    resultados = []
    
    # Obtener cotización para cada ticker
    for ticker in tickers:
        datos = obtener_cotizacion(ticker)
        if datos:  # Solo agregar los datos si no es None
            resultados.append(datos)
    
    # Pasar los datos a la plantilla
    return render_template('index.html', cotizaciones=resultados)

if __name__ == '__main__':
    app.run(debug=True)