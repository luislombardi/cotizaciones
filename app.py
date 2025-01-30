from flask import Flask, render_template
from views import cotizaciones_bp, volatilidad_bp

app = Flask(__name__)

app.register_blueprint(cotizaciones_bp)
app.register_blueprint(volatilidad_bp)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
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

if __name__ == '__main__':
    app.run(debug=True)
