from flask import Flask
from flask_cors import CORS
from routes import risk_bp

app = Flask(__name__)

# Enable CORS for all domains so your local HTML file can call the API
CORS(app)

# Register the blueprint we defined in routes.py
app.register_blueprint(risk_bp)

if __name__ == '__main__':
    print("Starting CareConnect Backend...")
    app.run(debug=True, port=5000)