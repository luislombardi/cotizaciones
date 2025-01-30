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

