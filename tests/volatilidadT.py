import yfinance as yf
import pandas as pd

def calcular_metricas(ticker):
    """Calcula métricas para un ticker usando .iloc para evitar errores de formato."""
    try:
        data = yf.download(ticker, period="14d")
        
        # Verificar que los datos no estén vacíos y contengan las columnas necesarias
        if data.empty or not all(col in data.columns for col in ['High', 'Low', 'Close']):
            return None  # Si no hay datos o faltan columnas, retorna None
        
        # Calcular métricas
        max_periodo = data['High'].max()
        min_periodo = data['Low'].min()
        
        # Obtener el último cierre usando .iloc[-1] (más robusto)
        ultimo_cierre = data['Close'].iloc[-1]
        
        # Convertir valores a escalares
        max_periodo = max_periodo.item()
        min_periodo = min_periodo.item()
        ultimo_cierre = ultimo_cierre.item()
        
        volatilidad = ((max_periodo - min_periodo) / ultimo_cierre) * 100
        
        return {
            'ticker': ticker,
            'Precio Cierre': f"${ultimo_cierre:.2f}",
            'Máximo 2s': f"${max_periodo:.2f}",
            'Mínimo 2s': f"${min_periodo:.2f}",
            'Volatilidad %': f"{volatilidad:.2f}%"
        }
    except KeyError as e:
        print(f"Error: Columna faltante en datos de {ticker}: {e}")
        return {
            'ticker': ticker,
            'Precio Cierre': "N/A",
            'Máximo 2s': "N/A",
            'Mínimo 2s': "N/A",
            'Volatilidad %': "N/A"
        }
    except Exception as e:
        print(f"Error procesando {ticker}: {e}")
        return {
            'ticker': ticker,
            'Precio Cierre': "N/A",
            'Máximo 2s': "N/A",
            'Mínimo 2s': "N/A",
            'Volatilidad %': "N/A"
        }

# Lista de activos a comparar
tickers = ["AAPL", "TSLA", "AMZN", "GOOGL"]

# Calcular métricas para cada activo
datos_tabla = []
for ticker in tickers:
    metricas = calcular_metricas(ticker)
    if metricas:
        datos_tabla.append(metricas)

# Crear DataFrame y mostrar tabla
df_tabla = pd.DataFrame(datos_tabla)
df_tabla.set_index('ticker', inplace=True)
print("\nTabla Comparativa de Activos (2 semanas):")
print(df_tabla.to_string())