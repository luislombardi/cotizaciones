
# Importación de bibliotecas
import yfinance as yf  # Para descargar datos históricos de Yahoo Finance
import pandas as pd    # Para manipular y analizar datos en formato DataFrame
import matplotlib.pyplot as plt  # Para crear gráficos

# Función para calcular el RSI
def calculate_rsi(data, period=30):  # Período de 30 días para mayor sensibilidad
    """Calcula el RSI para un conjunto de datos."""
    try:
        # Calcula la diferencia entre los precios de cierre consecutivos
        delta = data['Close'].diff()
        
        # Separa las subidas (up) y bajadas (down) en dos series
        up = delta.clip(lower=0)  # Solo valores positivos (subidas)
        down = -1 * delta.clip(upper=0)  # Solo valores negativos (bajadas)
        
        # Calcula la media móvil exponencial (EMA) de las subidas y bajadas
        ema_up = up.ewm(com=period - 1, adjust=False).mean()  # EMA de subidas
        ema_down = down.ewm(com=period - 1, adjust=False).mean()  # EMA de bajadas
        
        # Calcula el RSI usando la fórmula estándar
        rsi = 100 - (100 / (1 + (ema_up / ema_down)))
        
        return rsi  # Retorna la serie de valores del RSI
    except Exception as e:
        print(f"Error al calcular RSI: {e}")  # Manejo de errores
        return None

# Función para calcular el MACD
def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """Calcula el MACD y su línea de señal."""
    try:
        # Calcula las medias móviles exponenciales (EMA) de 12 y 26 días
        data['EMA12'] = data['Close'].ewm(span=short_window, adjust=False).mean()
        data['EMA26'] = data['Close'].ewm(span=long_window, adjust=False).mean()
        
        # Calcula el MACD (diferencia entre EMA12 y EMA26)
        data['MACD'] = data['EMA12'] - data['EMA26']
        
        # Calcula la línea de señal (EMA de 9 días del MACD)
        data['Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
        
        return data  # Retorna el DataFrame con el MACD y la línea de señal
    except Exception as e:
        print(f"Error al calcular MACD: {e}")  # Manejo de errores
        return None

# Función para graficar el precio de cierre, las medias móviles, el RSI, el MACD y la distancia entre medias
def plot_data(data, ticker, periodo_rsi=30):
    """Grafica el precio de cierre, las medias móviles, el RSI, el MACD y la distancia entre medias."""
    # Crea una figura con cuatro subgráficos
    plt.figure(figsize=(14, 16))  # Tamaño de la figura ajustado
    
    # Subgráfico 1: Precio de cierre y medias móviles
    plt.subplot(4, 1, 1)  # Cuatro filas, una columna, primer gráfico
    plt.plot(data['Close'], label=f'Precio de cierre ({ticker})', color='blue')  # Grafica el precio
    plt.plot(data['MA50'], label='Media Móvil 50 días', color='green', linestyle='--')  # Grafica la media de 50 días
    plt.plot(data['MA200'], label='Media Móvil 200 días', color='red', linestyle='--')  # Grafica la media de 200 días
    plt.title(f'Precio de {ticker} y Medias Móviles')  # Título del gráfico
    plt.legend()  # Muestra la leyenda
    
    # Subgráfico 2: RSI
    plt.subplot(4, 1, 2)  # Cuatro filas, una columna, segundo gráfico
    plt.plot(data['RSI'], label=f'RSI ({periodo_rsi})', color='orange')  # Grafica el RSI
    plt.axhline(70, color='red', linestyle='--', label='Sobrecompra (70)')  # Línea de sobrecompra
    plt.axhline(30, color='green', linestyle='--', label='Sobreventa (30)')  # Línea de sobreventa
    plt.title(f'RSI de {ticker}')  # Título del gráfico
    plt.legend()  # Muestra la leyenda
    
    # Subgráfico 3: MACD con histograma
    plt.subplot(4, 1, 3)  # Cuatro filas, una columna, tercer gráfico
    plt.plot(data['MACD'], label='MACD', color='purple')  # Grafica el MACD
    plt.plot(data['Signal'], label='Línea de Señal', color='gray', linestyle='--')  # Grafica la línea de señal
    plt.bar(data.index, data['MACD'] - data['Signal'], label='Histograma MACD', color='lightblue')  # Grafica el histograma
    plt.title('MACD con Histograma')  # Título del gráfico
    plt.legend()  # Muestra la leyenda
    
    # Subgráfico 4: Distancia porcentual entre medias móviles
    data['Distancia_%'] = ((data['MA50'] - data['MA200']) / data['MA200']) * 100  # Distancia porcentual
    plt.subplot(4, 1, 4)  # Cuatro filas, una columna, cuarto gráfico
    plt.plot(data['Distancia_%'], label='Distancia % entre MA50 y MA200', color='brown')  # Grafica la distancia
    plt.axhline(0, color='black', linestyle='--', label='Línea de referencia (0%)')  # Línea de referencia
    plt.title('Distancia porcentual entre MA50 y MA200')  # Título del gráfico
    plt.legend()  # Muestra la leyenda
    
    plt.tight_layout()  # Ajusta el espaciado entre subgráficos
    plt.show()  # Muestra la figura

# Símbolo del activo y período del RSI
ticker = "AAPL"  # Puedes cambiar el ticker (por ejemplo, "MSFT" para Microsoft)
periodo_rsi = 30  # Período del RSI para mayor sensibilidad

try:
    # Descarga los datos históricos de los últimos 5 años
    data = yf.download(ticker, period="5y")  # Descarga 5 años de datos para largo plazo
    
    # Calcula el RSI usando la función definida
    data['RSI'] = calculate_rsi(data, periodo_rsi)
    
    # Calcula las medias móviles de 50 y 200 días
    data['MA50'] = data['Close'].rolling(window=50).mean()  # Media móvil de 50 días
    data['MA200'] = data['Close'].rolling(window=200).mean()  # Media móvil de 200 días
    
    # Calcula el MACD y la línea de señal
    data = calculate_macd(data)
    
    # Si el RSI y el MACD se calcularon correctamente, grafica los datos
    if data['RSI'] is not None and data['MACD'] is not None:
        plot_data(data, ticker, periodo_rsi)  # Llama a la función para graficar
        print(data[['Close', 'MA50', 'MA200', 'RSI', 'MACD', 'Signal', 'Distancia_%']].tail())  # Imprime los últimos valores en la consola
except Exception as e:
    print(f"Error al descargar datos: {e}")  # Manejo de errores