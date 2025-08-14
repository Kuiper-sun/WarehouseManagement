from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    app.register_blueprint(api, url_prefix='/api')
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # The tables are created by init.sql, so create_all() is not strictly necessary
        # but it's good practice to have it in case you add more models later.
        pass
    app.run(host='0.0.0.0', port=5000, debug=True)