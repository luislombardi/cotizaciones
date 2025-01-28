# Logica del backend de la aplicacion

from flask import Flask, render_template, jsonify
import yfinance as yf

app = Flask(__name__)

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')  # Aquí puedes renderizar tu archivo HTML

# Función para obtener datos de cotización
def obtener_cotizacion(ticker):
    accion = yf.Ticker(ticker)
    datos = accion.history(period="1d")  # Obtener los datos de un día
    precio_cierre = datos["Close"].iloc[-1]  # Obtener el último precio de cierre
    return {
        "nombre": accion.info.get("shortName", "Desconocido"),
        "precio": precio_cierre
    }

@app.route('/cotizaciones')
def cotizaciones():
    tickers = ["AAPL", "GOOGL", "TSLA"]  # Lista de tickers
    resultados = []
    
    # Obtener cotización para cada ticker
    for ticker in tickers:
        datos = obtener_cotizacion(ticker)
        resultados.append(datos)
    
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)
