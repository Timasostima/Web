from flask import Flask
from mvc_endpoints import mvc_bp
from api_endpoints import api_bp

app = Flask(__name__)
app.register_blueprint(mvc_bp)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)
